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
``Sessions.interrupt_turn`` (sync and async) forwards the request, the metadata and the deadline to the stub.

The wrappers are generated (``make generate_services``); these tests pin that the generated code passes
``timeout`` through as the gRPC deadline and keeps ``None`` (no deadline) as the default. No channel is opened.
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

from ondewo.nlu import session_pb2
from ondewo.nlu.services.async_sessions import Sessions as AsyncSessions
from ondewo.nlu.services.sessions import Sessions

METADATA: List[Tuple[str, str]] = [("authorization", "Bearer planted")]
REQUEST: session_pb2.InterruptTurnRequest = session_pb2.InterruptTurnRequest(
    session="projects/p/agent/sessions/s",
    turn_control=session_pb2.TurnControl(cancel_turn=session_pb2.CancelTurn(client_turn_id="t-1")),
)
RESPONSE: session_pb2.InterruptTurnResponse = session_pb2.InterruptTurnResponse(
    turn_control_ack=session_pb2.TurnControlAck(
        client_turn_id="t-1",
        turn_control_ack_status=session_pb2.TURN_CONTROL_ACK_STATUS_CANCELLED,
    )
)


def _call_sync(stub: MagicMock, timeout: Optional[float], pass_timeout: bool) -> session_pb2.InterruptTurnResponse:
    """
    Call the sync wrapper on a service built without a channel.

    Args:
        stub (MagicMock):
            Stands in for the generated ``SessionsStub``.
        timeout (Optional[float]):
            The deadline to pass when ``pass_timeout`` is set.
        pass_timeout (bool):
            Whether to pass ``timeout`` at all (False exercises the default).

    Returns:
        session_pb2.InterruptTurnResponse:
            What the wrapper returned.
    """
    service: Sessions = object.__new__(Sessions)
    with (
        patch.object(Sessions, "stub", new_callable=PropertyMock, return_value=stub),
        patch.object(Sessions, "metadata", new_callable=PropertyMock, return_value=METADATA),
    ):
        if pass_timeout:
            return service.interrupt_turn(REQUEST, timeout=timeout)
        return service.interrupt_turn(REQUEST)


def _call_async(stub: MagicMock, timeout: Optional[float], pass_timeout: bool) -> session_pb2.InterruptTurnResponse:
    """
    Call the async wrapper on a service built without a channel.

    Args:
        stub (MagicMock):
            Stands in for the generated async ``SessionsStub``.
        timeout (Optional[float]):
            The deadline to pass when ``pass_timeout`` is set.
        pass_timeout (bool):
            Whether to pass ``timeout`` at all (False exercises the default).

    Returns:
        session_pb2.InterruptTurnResponse:
            What the wrapper returned.
    """
    service: AsyncSessions = object.__new__(AsyncSessions)

    async def scenario() -> session_pb2.InterruptTurnResponse:
        with (
            patch.object(AsyncSessions, "stub", new_callable=PropertyMock, return_value=stub),
            patch.object(AsyncSessions, "metadata", new_callable=PropertyMock, return_value=METADATA),
        ):
            if pass_timeout:
                return await service.interrupt_turn(REQUEST, timeout=timeout)
            return await service.interrupt_turn(REQUEST)

    return asyncio.run(scenario())


def _single_call_kwargs(rpc: Any) -> Dict[str, Any]:
    """
    Assert the stub RPC was called once with the request and return the keyword arguments.

    Args:
        rpc (Any):
            The mocked ``stub.InterruptTurn``.

    Returns:
        Dict[str, Any]:
            The keyword arguments of the single call.
    """
    rpc.assert_called_once()
    args, kwargs = rpc.call_args
    assert args == (REQUEST,)
    return dict(kwargs)


class TestSyncInterruptTurn:
    """The sync wrapper."""

    def test_passes_the_timeout_as_the_deadline(self) -> None:
        """``timeout`` reaches the stub call unchanged, next to the metadata."""
        stub = MagicMock()
        stub.InterruptTurn.return_value = RESPONSE
        assert _call_sync(stub, 0.25, pass_timeout=True) == RESPONSE
        assert _single_call_kwargs(stub.InterruptTurn) == {"metadata": METADATA, "timeout": 0.25}

    def test_defaults_to_no_deadline(self) -> None:
        """Without ``timeout`` the stub gets ``timeout=None``, gRPC's "no deadline"."""
        stub = MagicMock()
        stub.InterruptTurn.return_value = RESPONSE
        assert _call_sync(stub, None, pass_timeout=False) == RESPONSE
        assert _single_call_kwargs(stub.InterruptTurn) == {"metadata": METADATA, "timeout": None}


class TestAsyncInterruptTurn:
    """The async wrapper, derived from the sync one by ``create_async_services``."""

    def test_passes_the_timeout_as_the_deadline(self) -> None:
        """``timeout`` reaches the awaited stub call unchanged."""
        stub = MagicMock()
        stub.InterruptTurn = AsyncMock(return_value=RESPONSE)
        assert _call_async(stub, 1.5, pass_timeout=True) == RESPONSE
        assert _single_call_kwargs(stub.InterruptTurn) == {"metadata": METADATA, "timeout": 1.5}

    def test_defaults_to_no_deadline(self) -> None:
        """Without ``timeout`` the awaited stub call gets ``timeout=None``."""
        stub = MagicMock()
        stub.InterruptTurn = AsyncMock(return_value=RESPONSE)
        assert _call_async(stub, None, pass_timeout=False) == RESPONSE
        assert _single_call_kwargs(stub.InterruptTurn) == {"metadata": METADATA, "timeout": None}


class TestOtherWrappersKeepTheirSignature:
    """The deadline argument is opt-in: an unrelated wrapper takes no ``timeout``."""

    def test_detect_intent_takes_no_timeout(self) -> None:
        """``detect_intent`` still takes exactly ``request``."""
        assert Sessions.detect_intent.__code__.co_varnames[: Sessions.detect_intent.__code__.co_argcount] == (
            "self",
            "request",
        )
