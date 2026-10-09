# Copyright 2021-2025 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
TLS and mutual TLS end to end: the SDK's real clients against a real in-process gRPC server.

Every client this package ships (``Client``, ``AsyncClient``, the QA ``Client``, ``ClientPool``; per-service and
``use_shared_channel=True``) is built from the SDK's own ``ClientConfig`` and makes one real RPC. The server has no
servicer, so ``UNIMPLEMENTED`` proves the request crossed a completed TLS handshake; ``UNAVAILABLE`` is a refused
one. Certificates are minted per module (one deployment CA, one unrelated CA); no private key is committed.

The RPCs used (``CreateAgent``, ``RunTraining``) are non-idempotent, so the SDK's retry policy does not retry a
refused handshake and a refusal surfaces at once instead of after the retry budget.
"""

import asyncio
import dataclasses
import datetime
import ipaddress
import socket
from concurrent import futures
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
)
from unittest import mock

import grpc
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import (
    hashes,
    serialization,
)
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import (
    ExtendedKeyUsageOID,
    NameOID,
)

from ondewo.nlu.agent_pb2 import (
    Agent,
    CreateAgentRequest,
)
from ondewo.nlu.async_client import AsyncClient
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.client_pool import ClientPool
from ondewo.qa.client import Client as QaClient
from ondewo.qa.client_config import ClientConfig as QaClientConfig

PASSWORD: str = "s3cr3t-password"
REQUEST: CreateAgentRequest = CreateAgentRequest(agent=Agent(display_name="tls"))

StartServer = Callable[..., int]


class Pki:
    """One throwaway CA with a server leaf (SAN localhost, 127.0.0.1, ::1) and a client leaf, all PEM str."""

    def __init__(self, name: str) -> None:
        self._ca_key: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP256R1())
        ca_name: x509.Name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, f"{name}-ca")])
        self._ca: x509.Certificate = self._issue(ca_name, ca_name, self._ca_key.public_key(), ca=True)
        self.ca_cert: str = self._ca.public_bytes(serialization.Encoding.PEM).decode()
        self.server_key, self.server_cert = self._leaf(f"{name}-server", ExtendedKeyUsageOID.SERVER_AUTH, san=True)
        self.client_key, self.client_cert = self._leaf(f"{name}-client", ExtendedKeyUsageOID.CLIENT_AUTH, san=False)

    def _leaf(self, subject: str, usage: x509.ObjectIdentifier, san: bool) -> "tuple[str, str]":
        key: ec.EllipticCurvePrivateKey = ec.generate_private_key(ec.SECP256R1())
        name: x509.Name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, subject)])
        cert: x509.Certificate = self._issue(name, self._ca.subject, key.public_key(), ca=False, usage=usage, san=san)
        pem_key: str = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode()
        return pem_key, cert.public_bytes(serialization.Encoding.PEM).decode()

    def _issue(
        self,
        subject: x509.Name,
        issuer: x509.Name,
        public_key: ec.EllipticCurvePublicKey,
        ca: bool,
        usage: Optional[x509.ObjectIdentifier] = None,
        san: bool = False,
    ) -> x509.Certificate:
        now: datetime.datetime = datetime.datetime.now(datetime.timezone.utc)
        builder: x509.CertificateBuilder = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(public_key)
            .serial_number(x509.random_serial_number())
            .not_valid_before(now - datetime.timedelta(days=1))
            .not_valid_after(now + datetime.timedelta(days=30))
            .add_extension(x509.BasicConstraints(ca=ca, path_length=None), critical=True)
        )
        if usage is not None:
            builder = builder.add_extension(x509.ExtendedKeyUsage([usage]), critical=False)
        if san:
            builder = builder.add_extension(
                x509.SubjectAlternativeName(
                    [
                        x509.DNSName("localhost"),
                        x509.IPAddress(ipaddress.ip_address("127.0.0.1")),
                        x509.IPAddress(ipaddress.ip_address("::1")),
                    ]
                ),
                critical=False,
            )
        return builder.sign(self._ca_key, hashes.SHA256())


@pytest.fixture(scope="module")
def pki() -> Pki:
    return Pki("deployment")


@pytest.fixture(scope="module")
def foreign() -> Pki:
    return Pki("foreign")


def _server_credentials(pki: Pki, require_client_auth: bool) -> grpc.ServerCredentials:
    return grpc.ssl_server_credentials(
        [(pki.server_key.encode(), pki.server_cert.encode())],
        root_certificates=pki.ca_cert.encode() if require_client_auth else None,
        require_client_auth=require_client_auth,
    )


@pytest.fixture
def server() -> Iterator[StartServer]:
    """Start a servicer-less TLS server; ``(pki, require_client_auth, bind="localhost") -> port``."""
    servers: List[grpc.Server] = []

    def start(pki: Pki, require_client_auth: bool, bind: str = "localhost") -> int:
        grpc_server: grpc.Server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        port: int = grpc_server.add_secure_port(f"{bind}:0", _server_credentials(pki, require_client_auth))
        grpc_server.start()
        servers.append(grpc_server)
        return port

    yield start
    for grpc_server in servers:
        grpc_server.stop(grace=None)


def _config(
    port: int,
    trust: Pki,
    identity: Optional[Pki] = None,
    host: str = "localhost",
) -> ClientConfig:
    """The SDK's own config (non-Keycloak path) trusting ``trust``'s CA, presenting ``identity``'s leaf if given."""
    return ClientConfig(
        host=host,
        port=str(port),
        grpc_cert=trust.ca_cert,
        grpc_client_cert=None if identity is None else identity.client_cert,
        grpc_client_key=None if identity is None else identity.client_key,
        user_name="tls@ondewo.com",
        password=PASSWORD,
    )


def _sync_call(config: ClientConfig, use_shared_channel: bool) -> grpc.StatusCode:
    client: Client = Client(config=config, use_secure_channel=True, use_shared_channel=use_shared_channel)
    try:
        with pytest.raises(grpc.RpcError) as error:
            client.services.agents.create_agent(REQUEST)
        code: grpc.StatusCode = error.value.code()  # type: ignore[attr-defined]
        return code
    finally:
        client.disconnect()


def _async_call(config: ClientConfig, use_shared_channel: bool, pki: Pki, require_client_auth: bool) -> grpc.StatusCode:
    async def scenario() -> grpc.StatusCode:
        aio_server: grpc.aio.Server = grpc.aio.server()
        port: int = aio_server.add_secure_port("localhost:0", _server_credentials(pki, require_client_auth))
        await aio_server.start()
        client: AsyncClient = AsyncClient(
            config=dataclasses.replace(config, port=str(port)),
            use_secure_channel=True,
            use_shared_channel=use_shared_channel,
        )
        try:
            with pytest.raises(grpc.aio.AioRpcError) as error:
                await client.services.agents.create_agent(REQUEST)
            return error.value.code()
        finally:
            await client.disconnect()  # type: ignore[func-returns-value]
            await aio_server.stop(grace=None)

    return asyncio.run(scenario())


SHARED: List[bool] = [False, True]


@pytest.mark.parametrize("use_shared_channel", SHARED)
class TestClient:
    def test_plain_tls_reaches_the_server(self, server: StartServer, pki: Pki, use_shared_channel: bool) -> None:
        port: int = server(pki, False)
        assert _sync_call(_config(port, pki), use_shared_channel) is grpc.StatusCode.UNIMPLEMENTED

    def test_mutual_tls_reaches_the_server(self, server: StartServer, pki: Pki, use_shared_channel: bool) -> None:
        port: int = server(pki, True)
        assert _sync_call(_config(port, pki, pki), use_shared_channel) is grpc.StatusCode.UNIMPLEMENTED

    def test_no_identity_against_a_client_auth_server_is_refused(
        self, server: StartServer, pki: Pki, use_shared_channel: bool
    ) -> None:
        port: int = server(pki, True)
        assert _sync_call(_config(port, pki), use_shared_channel) is grpc.StatusCode.UNAVAILABLE

    def test_an_identity_from_an_unrelated_ca_is_refused(
        self, server: StartServer, pki: Pki, foreign: Pki, use_shared_channel: bool
    ) -> None:
        port: int = server(pki, True)
        assert _sync_call(_config(port, pki, foreign), use_shared_channel) is grpc.StatusCode.UNAVAILABLE

    def test_a_server_from_an_untrusted_ca_is_refused(
        self, server: StartServer, pki: Pki, foreign: Pki, use_shared_channel: bool
    ) -> None:
        port: int = server(pki, True)
        assert _sync_call(_config(port, foreign, pki), use_shared_channel) is grpc.StatusCode.UNAVAILABLE

    def test_tls_only_server_also_serves_a_client_presenting_an_identity(
        self, server: StartServer, pki: Pki, use_shared_channel: bool
    ) -> None:
        port: int = server(pki, False)
        assert _sync_call(_config(port, pki, pki), use_shared_channel) is grpc.StatusCode.UNIMPLEMENTED

    def test_crlf_pems_complete_the_mutual_tls_handshake(
        self, server: StartServer, pki: Pki, use_shared_channel: bool
    ) -> None:
        port: int = server(pki, True)
        crlf: Callable[[str], str] = lambda pem: pem.replace("\n", "\r\n")  # noqa: E731
        config: ClientConfig = ClientConfig(
            host="localhost",
            port=str(port),
            grpc_cert=crlf(pki.ca_cert),
            grpc_client_cert=crlf(pki.client_cert),
            grpc_client_key=crlf(pki.client_key),
            user_name="tls@ondewo.com",
            password=PASSWORD,
        )
        assert _sync_call(config, use_shared_channel) is grpc.StatusCode.UNIMPLEMENTED

    def test_empty_strings_on_both_mean_plain_tls(
        self, server: StartServer, pki: Pki, use_shared_channel: bool
    ) -> None:
        port: int = server(pki, False)
        config: ClientConfig = ClientConfig(
            host="localhost",
            port=str(port),
            grpc_cert=pki.ca_cert,
            grpc_client_cert="",
            grpc_client_key="",
            user_name="tls@ondewo.com",
            password=PASSWORD,
        )
        assert _sync_call(config, use_shared_channel) is grpc.StatusCode.UNIMPLEMENTED

    def test_mutual_tls_over_ipv6(self, server: StartServer, pki: Pki, use_shared_channel: bool) -> None:
        if not socket.has_ipv6:
            pytest.skip("no IPv6 on this host")
        try:
            port: int = server(pki, True, bind="[::1]")
        except RuntimeError:
            pytest.skip("cannot bind [::1] on this host")
        config: ClientConfig = _config(port, pki, pki, host="::1")
        assert config.host_and_port == f"[::1]:{port}"
        assert _sync_call(config, use_shared_channel) is grpc.StatusCode.UNIMPLEMENTED


@pytest.mark.parametrize("use_shared_channel", SHARED)
class TestAsyncClient:
    def test_plain_tls_reaches_the_server(self, pki: Pki, use_shared_channel: bool) -> None:
        code: grpc.StatusCode = _async_call(_config(0, pki), use_shared_channel, pki, False)
        assert code is grpc.StatusCode.UNIMPLEMENTED

    def test_mutual_tls_reaches_the_server(self, pki: Pki, use_shared_channel: bool) -> None:
        code: grpc.StatusCode = _async_call(_config(0, pki, pki), use_shared_channel, pki, True)
        assert code is grpc.StatusCode.UNIMPLEMENTED

    def test_no_identity_against_a_client_auth_server_is_refused(self, pki: Pki, use_shared_channel: bool) -> None:
        code: grpc.StatusCode = _async_call(_config(0, pki), use_shared_channel, pki, True)
        assert code is grpc.StatusCode.UNAVAILABLE

    def test_an_identity_from_an_unrelated_ca_is_refused(
        self, pki: Pki, foreign: Pki, use_shared_channel: bool
    ) -> None:
        code: grpc.StatusCode = _async_call(_config(0, pki, foreign), use_shared_channel, pki, True)
        assert code is grpc.StatusCode.UNAVAILABLE


@pytest.mark.parametrize("use_shared_channel", SHARED)
class TestQaClient:
    @staticmethod
    def _call(port: int, pki: Pki, identity: Optional[Pki], use_shared_channel: bool) -> grpc.StatusCode:
        config: QaClientConfig = QaClientConfig(
            host="localhost",
            port=str(port),
            grpc_cert=pki.ca_cert,
            grpc_client_cert=None if identity is None else identity.client_cert,
            grpc_client_key=None if identity is None else identity.client_key,
        )
        client: QaClient = QaClient(config=config, use_secure_channel=True, use_shared_channel=use_shared_channel)
        try:
            with pytest.raises(grpc.RpcError) as error:
                client.services.qa.run_training()
            code: grpc.StatusCode = error.value.code()  # type: ignore[attr-defined]
            return code
        finally:
            client.disconnect()

    def test_mutual_tls_reaches_the_server(self, server: StartServer, pki: Pki, use_shared_channel: bool) -> None:
        port: int = server(pki, True)
        assert self._call(port, pki, pki, use_shared_channel) is grpc.StatusCode.UNIMPLEMENTED

    def test_no_identity_against_a_client_auth_server_is_refused(
        self, server: StartServer, pki: Pki, use_shared_channel: bool
    ) -> None:
        port: int = server(pki, True)
        assert self._call(port, pki, None, use_shared_channel) is grpc.StatusCode.UNAVAILABLE

    def test_an_identity_from_an_unrelated_ca_is_refused(
        self, server: StartServer, pki: Pki, foreign: Pki, use_shared_channel: bool
    ) -> None:
        port: int = server(pki, True)
        assert self._call(port, pki, foreign, use_shared_channel) is grpc.StatusCode.UNAVAILABLE


@pytest.mark.parametrize("use_shared_channel", SHARED)
def test_client_pool_clients_complete_mutual_tls(server: StartServer, pki: Pki, use_shared_channel: bool) -> None:
    port: int = server(pki, True)
    pool: ClientPool = ClientPool(config=_config(port, pki, pki), pool_size=1, use_shared_channel=use_shared_channel)
    client: Client = pool.acquire_client()
    try:
        with pytest.raises(grpc.RpcError) as error:
            client.services.agents.create_agent(REQUEST)
        assert error.value.code() is grpc.StatusCode.UNIMPLEMENTED  # type: ignore[attr-defined]
    finally:
        client.disconnect()


class TestConfigurationErrors:
    @pytest.mark.parametrize("half", ["grpc_client_cert", "grpc_client_key"])
    def test_half_a_client_identity_is_refused_before_grpc(self, pki: Pki, half: str) -> None:
        pems: Dict[str, Any] = {half: pki.client_cert if half == "grpc_client_cert" else pki.client_key}
        with mock.patch("grpc.ssl_channel_credentials") as credentials:
            with pytest.raises(ValueError, match="set both to use mutual TLS, or neither") as refusal:
                ClientConfig(
                    host="localhost",
                    port="1",
                    grpc_cert=pki.ca_cert,
                    user_name="tls@ondewo.com",
                    password=PASSWORD,
                    **pems,
                )
        credentials.assert_not_called()
        assert "BEGIN" not in str(refusal.value)
        assert PASSWORD not in str(refusal.value)

    @pytest.mark.parametrize("use_shared_channel", SHARED)
    def test_an_insecure_channel_with_an_identity_is_refused(self, pki: Pki, use_shared_channel: bool) -> None:
        with mock.patch("grpc.insecure_channel") as insecure:
            with pytest.raises(ValueError, match="use a secure channel") as refusal:
                Client(config=_config(1, pki, pki), use_secure_channel=False, use_shared_channel=use_shared_channel)
        insecure.assert_not_called()
        message: str = str(refusal.value)
        assert "BEGIN" not in message
        assert PASSWORD not in message
        assert "localhost:1" in message

    def test_an_insecure_async_channel_with_an_identity_is_refused(self, pki: Pki) -> None:
        with pytest.raises(ValueError, match="use a secure channel"):
            AsyncClient(config=_config(1, pki, pki), use_secure_channel=False)

    def test_the_config_repr_never_renders_the_key_or_the_password(self, pki: Pki) -> None:
        config: ClientConfig = _config(1, pki, pki)
        for rendered in (repr(config), str(config)):
            assert pki.client_key.strip().splitlines()[1] not in rendered
            assert "PRIVATE KEY" not in rendered
            assert PASSWORD not in rendered

    def test_the_qa_config_repr_never_renders_the_key(self, pki: Pki) -> None:
        config: QaClientConfig = QaClientConfig(
            host="localhost",
            port="1",
            grpc_cert=pki.ca_cert,
            grpc_client_cert=pki.client_cert,
            grpc_client_key=pki.client_key,
        )
        for rendered in (repr(config), str(config)):
            assert "PRIVATE KEY" not in rendered
