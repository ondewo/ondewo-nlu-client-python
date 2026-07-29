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
"""Hermetic guards on the public `Users` service surface after the 7.0.0 `Login` removal.

The 7.0.0 API dropped the `Login` RPC together with `LoginRequest` / `LoginResponse` and
`POST /v2/login`; authentication is Keycloak bearer only (see `test_auth_wiring.py`).
`CheckLogin` is a *different* RPC and is deliberately KEPT — these tests pin both halves so a
future cleanup can neither resurrect `Login` nor mistake `CheckLogin` for a leftover of it.

The import guard exists because of a specific, repeatable release trap: the `*_pb2.py` family and
`ondewo/nlu/services/*.py` come from **two different generators** (`make generate_ondewo_protos`
vs. `make generate_services`). Running only the first after a message REMOVAL leaves
`services/users.py` importing a name `user_pb2` no longer defines, and `async_users.py` /
`async_client.py` are derived from it. The failure is an **ImportError at import time**, not at
call time, so the whole SDK becomes unimportable — `import ondewo.nlu.client` is enough to trip it.
Adding a field is forgiving; removing one is not.

No network is touched: nothing here constructs a client or opens a channel.
"""

import subprocess
import sys
from pathlib import Path
from typing import (
    List,
    Tuple,
)

from ondewo.nlu import user_pb2
from ondewo.nlu.services.async_users import Users as AsyncUsers
from ondewo.nlu.services.users import Users

# Bound once so a refactor that changes only an input or only an expectation cannot silently
# make an assertion tautological.
REMOVED_METHOD: str = "login"
KEPT_METHOD: str = "check_login"
REMOVED_MESSAGES: Tuple[str, ...] = ("LoginRequest", "LoginResponse")
REMOVED_RPC: str = "Login"
KEPT_RPC: str = "CheckLogin"
USERS_SERVICE: str = "Users"

REPO_ROOT: Path = Path(__file__).resolve().parents[3]


class TestLoginIsGoneFromTheServiceSurface:
    """Neither the sync nor the async `Users` service exposes the removed `login` method."""

    def test_sync_users_has_no_login_method(self) -> None:
        """`Users.login` was removed with the 7.0.0 API and must not come back."""
        assert not hasattr(Users, REMOVED_METHOD)

    def test_async_users_has_no_login_method(self) -> None:
        """`async_users.Users.login` is regenerated from the sync half and must stay absent."""
        assert not hasattr(AsyncUsers, REMOVED_METHOD)


class TestCheckLoginIsKept:
    """`CheckLogin` survives the `Login` removal on both service halves."""

    def test_sync_users_has_check_login_method(self) -> None:
        """`Users.check_login` is a separate, still-supported RPC."""
        assert hasattr(Users, KEPT_METHOD)

    def test_async_users_has_check_login_method(self) -> None:
        """`async_users.Users.check_login` mirrors the sync half."""
        assert hasattr(AsyncUsers, KEPT_METHOD)


class TestLoginMessagesAreGoneFromTheProto:
    """The generated `user_pb2` module carries no `Login` request/response pair or RPC."""

    def test_user_pb2_has_no_login_request_or_response(self) -> None:
        """`LoginRequest` / `LoginResponse` were deleted from `user.proto` at 7.0.0."""
        present: List[str] = [name for name in REMOVED_MESSAGES if hasattr(user_pb2, name)]

        assert present == []

    def test_users_service_descriptor_has_no_login_rpc_but_keeps_check_login(self) -> None:
        """The descriptor is the source of truth: `Login` is gone, `CheckLogin` remains.

        Checked against the descriptor rather than the module attributes because a stale
        regeneration can leave a Python symbol behind that the proto no longer declares.
        """
        rpc_names: List[str] = [method.name for method in user_pb2.DESCRIPTOR.services_by_name[USERS_SERVICE].methods]

        assert REMOVED_RPC not in rpc_names
        assert KEPT_RPC in rpc_names


class TestSdkIsImportable:
    """The package imports cleanly — the exact breakage a partial regeneration causes."""

    def test_client_imports_in_a_fresh_interpreter(self) -> None:
        """`from ondewo.nlu.client import Client` must succeed in a cold process.

        Run out-of-process on purpose: by the time this module is collected the in-process
        import cache already holds `ondewo.nlu.*`, so an in-process import would pass even
        against a half-regenerated tree. A fresh interpreter is what a consumer actually does.
        """
        result: subprocess.CompletedProcess = subprocess.run(
            [sys.executable, "-c", "from ondewo.nlu.client import Client; print(Client.__name__)"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0, f"importing the SDK failed:\n{result.stderr}"
        assert result.stdout.strip() == "Client"
