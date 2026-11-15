# Copyright 2021-2026 ONDEWO GmbH
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
``Sessions.prepare_warm_transfer_intro`` and ``Sessions.get_warm_transfer_intro_outcome`` (sync and async).

ondewo-vtsi calls both from bounded paths: Prepare inside a 6 s budget before the transfer target rings, the outcome
on its watcher's 1 s tick. Both wrappers therefore take an optional ``timeout`` (the gRPC deadline in seconds,
``None`` = no deadline) and forward it with the request and the metadata. No channel is opened.
"""

import asyncio
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
)
from unittest.mock import (
    AsyncMock,
    MagicMock,
    PropertyMock,
    patch,
)

import pytest
from google.protobuf.message import Message

from ondewo.nlu import session_pb2
from ondewo.nlu.services.async_sessions import Sessions as AsyncSessions
from ondewo.nlu.services.sessions import Sessions

METADATA: List[Tuple[str, str]] = [("authorization", "Bearer planted")]
INTRO_SESSION: str = "projects/p/agent/sessions/intro"

# (wrapper method, stub RPC name, request, response)
CASES: List[Tuple[str, str, Message, Message]] = [
    (
        "prepare_warm_transfer_intro",
        "PrepareWarmTransferIntro",
        session_pb2.PrepareWarmTransferIntroRequest(
            intro_session=INTRO_SESSION,
            source_session="projects/p/agent/sessions/source",
            transfer_request_id="t-1",
        ),
        session_pb2.PrepareWarmTransferIntroResponse(
            text_source_used=session_pb2.WARM_TRANSFER_INTRO_TEXT_SOURCE_TEMPLATE,
            intro_text_chars=42,
        ),
    ),
    (
        "get_warm_transfer_intro_outcome",
        "GetWarmTransferIntroOutcome",
        session_pb2.GetWarmTransferIntroOutcomeRequest(intro_session=INTRO_SESSION),
        session_pb2.WarmTransferIntroOutcome(
            decision=session_pb2.WARM_TRANSFER_INTRO_DECISION_ACCEPTED,
            decided_by=session_pb2.WARM_TRANSFER_INTRO_DECIDED_BY_DTMF,
        ),
    ),
]
CASE_IDS: List[str] = [case[0] for case in CASES]


def _call_sync(method: str, stub: MagicMock, request: Message, timeout: Optional[float], pass_timeout: bool) -> Any:
    """
    Call a sync wrapper on a service built without a channel.

    Args:
        method (str):
            The wrapper method name.
        stub (MagicMock):
            Stands in for the generated ``SessionsStub``.
        request (Message):
            The request to pass.
        timeout (Optional[float]):
            The deadline to pass when ``pass_timeout`` is set.
        pass_timeout (bool):
            Whether to pass ``timeout`` at all (False exercises the default).

    Returns:
        Any:
            What the wrapper returned.
    """
    service: Sessions = object.__new__(Sessions)
    with (
        patch.object(Sessions, "stub", new_callable=PropertyMock, return_value=stub),
        patch.object(Sessions, "metadata", new_callable=PropertyMock, return_value=METADATA),
    ):
        if pass_timeout:
            return getattr(service, method)(request, timeout=timeout)
        return getattr(service, method)(request)


def _call_async(method: str, stub: MagicMock, request: Message, timeout: Optional[float], pass_timeout: bool) -> Any:
    """
    Call an async wrapper on a service built without a channel.

    Args:
        method (str):
            The wrapper method name.
        stub (MagicMock):
            Stands in for the generated async ``SessionsStub``.
        request (Message):
            The request to pass.
        timeout (Optional[float]):
            The deadline to pass when ``pass_timeout`` is set.
        pass_timeout (bool):
            Whether to pass ``timeout`` at all (False exercises the default).

    Returns:
        Any:
            What the wrapper returned.
    """
    service: AsyncSessions = object.__new__(AsyncSessions)

    async def scenario() -> Any:
        with (
            patch.object(AsyncSessions, "stub", new_callable=PropertyMock, return_value=stub),
            patch.object(AsyncSessions, "metadata", new_callable=PropertyMock, return_value=METADATA),
        ):
            if pass_timeout:
                return await getattr(service, method)(request, timeout=timeout)
            return await getattr(service, method)(request)

    return asyncio.run(scenario())


def _single_call_kwargs(rpc: Any, request: Message) -> Dict[str, Any]:
    """
    Assert the stub RPC was called once with the request and return the keyword arguments.

    Args:
        rpc (Any):
            The mocked stub RPC.
        request (Message):
            The request the wrapper was given.

    Returns:
        Dict[str, Any]:
            The keyword arguments of the single call.
    """
    rpc.assert_called_once()
    args, kwargs = rpc.call_args
    assert args == (request,)
    return dict(kwargs)


class TestSyncWrappers:
    """The sync wrappers."""

    @pytest.mark.parametrize(("method", "rpc", "request_message", "response"), CASES, ids=CASE_IDS)
    def test_passes_the_timeout_as_the_deadline(
        self, method: str, rpc: str, request_message: Message, response: Message
    ) -> None:
        """``timeout`` reaches the stub call unchanged, next to the metadata."""
        stub = MagicMock()
        getattr(stub, rpc).return_value = response
        assert _call_sync(method, stub, request_message, 6.0, pass_timeout=True) == response
        assert _single_call_kwargs(getattr(stub, rpc), request_message) == {"metadata": METADATA, "timeout": 6.0}

    @pytest.mark.parametrize(("method", "rpc", "request_message", "response"), CASES, ids=CASE_IDS)
    def test_defaults_to_no_deadline(self, method: str, rpc: str, request_message: Message, response: Message) -> None:
        """Without ``timeout`` the stub gets ``timeout=None``, gRPC's "no deadline"."""
        stub = MagicMock()
        getattr(stub, rpc).return_value = response
        assert _call_sync(method, stub, request_message, None, pass_timeout=False) == response
        assert _single_call_kwargs(getattr(stub, rpc), request_message) == {"metadata": METADATA, "timeout": None}


class TestAsyncWrappers:
    """The async wrappers, derived from the sync ones by ``create_async_services``."""

    @pytest.mark.parametrize(("method", "rpc", "request_message", "response"), CASES, ids=CASE_IDS)
    def test_passes_the_timeout_as_the_deadline(
        self, method: str, rpc: str, request_message: Message, response: Message
    ) -> None:
        """``timeout`` reaches the awaited stub call unchanged."""
        stub = MagicMock()
        setattr(stub, rpc, AsyncMock(return_value=response))
        assert _call_async(method, stub, request_message, 1.0, pass_timeout=True) == response
        assert _single_call_kwargs(getattr(stub, rpc), request_message) == {"metadata": METADATA, "timeout": 1.0}

    @pytest.mark.parametrize(("method", "rpc", "request_message", "response"), CASES, ids=CASE_IDS)
    def test_defaults_to_no_deadline(self, method: str, rpc: str, request_message: Message, response: Message) -> None:
        """Without ``timeout`` the awaited stub call gets ``timeout=None``."""
        stub = MagicMock()
        setattr(stub, rpc, AsyncMock(return_value=response))
        assert _call_async(method, stub, request_message, None, pass_timeout=False) == response
        assert _single_call_kwargs(getattr(stub, rpc), request_message) == {"metadata": METADATA, "timeout": None}
