"""The Keycloak token refresh survives every failure, backs off, and never stalls or leaks.

This module is shared VERBATIM by every ondewo python client SDK (nlu, csi, s2t, sip, survey, t2s,
vtsi); only the import of the keycloak module differs. It pins the refresh handling those SDKs share:

* a failed refresh never ends the background refresh thread (it used to: one transient answer from
  the token endpoint let every token lapse for the life of the process);
* failures back off with full jitter from 5 s up to 300 s, and the lazy per-call path honours the
  SAME backoff, so an outage never turns every gRPC call into a token request under the lock;
* a token that is still valid keeps being served while its refresh fails; only an EXPIRED token
  raises, and it raises ``KeycloakAuthenticationError`` whatever went wrong underneath;
* no failure is ever answered with a password grant, and no credential reaches a log line.
"""

import threading
import time
import types
import weakref
from typing import Any, Dict, Iterator, List, Optional, Union

import pytest
import requests
from loguru import logger

from ondewo.nlu.utils import keycloak as km
from ondewo.nlu.utils.keycloak import KeycloakAuthenticationError, KeycloakTokenProvider

KEYCLOAK_URL: str = "https://keycloak.example/auth"
REALM: str = "ondewo-test-realm"
CLIENT_ID: str = "ondewo-test-sdk-public"
USERNAME: str = "technical-user@example.com"
PASSWORD: str = "pw-never-logged-5d1c"
DEAD_SESSION: Dict[str, str] = {"error": "invalid_grant", "error_description": "Offline user session not found"}


class FakeResponse:
    """A scripted token-endpoint answer."""

    def __init__(self, status_code: int, body: Any = None, text: Optional[str] = None) -> None:
        self.status_code: int = status_code
        self._body: Any = body
        self.text: str = text if text is not None else str(body)

    def json(self) -> Any:
        """Return the scripted body, or raise like requests does on a non-JSON body."""
        if isinstance(self._body, BaseException):
            raise self._body
        return self._body


Step = Union[FakeResponse, BaseException]


class FakeTransport:
    """Replays scripted answers (or raises scripted exceptions) and records every request form."""

    def __init__(self, steps: List[Step], delay_s: float = 0.0) -> None:
        self._steps: List[Step] = list(steps)
        self._delay_s: float = delay_s
        self._lock: threading.Lock = threading.Lock()
        self.calls: List[Dict[str, str]] = []

    def post(self, url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
        """Record the form and play the next step; the last step repeats once the script runs out."""
        with self._lock:
            self.calls.append(dict(data))
            step: Step = self._steps.pop(0) if len(self._steps) > 1 else self._steps[0]
        if self._delay_s:
            time.sleep(self._delay_s)
        if isinstance(step, BaseException):
            raise step
        return step

    def grants(self) -> List[str]:
        """The grant_type of every request so far."""
        return [call.get("grant_type", "") for call in self.calls]


class ScriptedEvent:
    """A ``threading.Event`` stand-in that drives ``_refresh_loop`` deterministically.

    ``wait(timeout)`` records the delay, advances the fake clock by it (or by a scripted amount) and
    replays a queued result (``True`` = stop fired, ``False`` = timed out, i.e. refresh). Once the
    script is exhausted it returns ``True`` so the loop ends and no test sleeps for real.
    """

    def __init__(
        self, wait_returns: List[bool], clock: Dict[str, float], advance_by: Optional[List[float]] = None
    ) -> None:
        self._wait_returns: List[bool] = list(wait_returns)
        self._clock: Dict[str, float] = clock
        self._advance_by: Optional[List[float]] = list(advance_by) if advance_by is not None else None
        self._set: bool = False
        self.wait_delays: List[float] = []

    def is_set(self) -> bool:
        return self._set

    def set(self) -> None:
        self._set = True

    def wait(self, timeout: Optional[float] = None) -> bool:
        self.wait_delays.append(float(timeout or 0.0))
        if self._advance_by:
            self._clock["now"] += self._advance_by.pop(0)
        elif timeout is not None:
            self._clock["now"] += timeout
        if not self._wait_returns:
            self._set = True
            return True
        result: bool = self._wait_returns.pop(0)
        self._set = self._set or result
        return result


def token(access: str, expires_in: Any = 300, refresh: Optional[str] = "off-x") -> FakeResponse:
    """A successful token response."""
    body: Dict[str, Any] = {"access_token": access, "expires_in": expires_in}
    if refresh is not None:
        body["refresh_token"] = refresh
    return FakeResponse(200, body)


def refused(status: int = 400, body: Optional[Dict[str, str]] = None) -> FakeResponse:
    """A refused token request (the dead offline session by default)."""
    return FakeResponse(status, body if body is not None else DEAD_SESSION)


def build(
    transport: FakeTransport,
    clock: Dict[str, float],
    stop_event: Optional[ScriptedEvent] = None,
    jitter: float = 0.0,
    token_expiration_in_s: Optional[int] = None,
) -> KeycloakTokenProvider:
    """A logged-in provider on a fake clock with a fixed jitter fraction and no background thread."""
    return KeycloakTokenProvider(
        keycloak_url=KEYCLOAK_URL,
        realm=REALM,
        client_id=CLIENT_ID,
        username=USERNAME,
        password=PASSWORD,
        token_expiration_in_s=token_expiration_in_s,
        transport=transport,  # type: ignore[arg-type]
        time_fn=lambda: clock["now"],
        random_fn=lambda: jitter,
        stop_event=stop_event if stop_event is not None else threading.Event(),  # type: ignore[arg-type]
        start_background_refresh=False,
    )


def run_loop(provider: KeycloakTokenProvider, event: ScriptedEvent, clock: Dict[str, float]) -> None:
    """Drive the real background loop body on the scripted event."""
    km._refresh_loop(weakref.ref(provider), event, lambda: clock["now"])  # type: ignore[arg-type]


@pytest.fixture
def records() -> Iterator[List[str]]:
    """Every loguru record emitted while the test runs, rendered with its level."""
    captured: List[str] = []
    sink_id: int = logger.add(lambda message: captured.append(str(message)), level="TRACE", format="{level} {message}")
    yield captured
    logger.remove(sink_id)


class TestTheBackoffLadder:
    """``_backoff_delay_s``: full jitter over a doubling window, capped, robust to bad input."""

    def test_the_ceiling_doubles_from_the_base_and_stops_at_the_maximum(self) -> None:
        delays: List[float] = [km._backoff_delay_s(n, lambda: 1.0) for n in range(1, 11)]
        assert delays == [5.0, 10.0, 20.0, 40.0, 80.0, 160.0, 300.0, 300.0, 300.0, 300.0]

    def test_a_zero_fraction_always_waits_the_base(self) -> None:
        assert {km._backoff_delay_s(n, lambda: 0.0) for n in range(1, 20)} == {km._REFRESH_RETRY_BASE_DELAY_S}

    def test_the_delay_is_drawn_inside_the_window(self) -> None:
        assert km._backoff_delay_s(2, lambda: 0.5) == 7.5
        assert km._backoff_delay_s(3, lambda: 0.25) == 8.75

    @pytest.mark.parametrize("fraction", [-1.0, -0.001, 1.5, 1e9])
    def test_a_faulty_jitter_source_is_clamped_into_the_window(self, fraction: float) -> None:
        delay: float = km._backoff_delay_s(4, lambda: fraction)
        assert km._REFRESH_RETRY_BASE_DELAY_S <= delay <= 40.0

    @pytest.mark.parametrize("failures", [0, -3])
    def test_a_non_positive_failure_count_is_treated_as_the_first_failure(self, failures: int) -> None:
        assert km._backoff_delay_s(failures, lambda: 1.0) == km._REFRESH_RETRY_BASE_DELAY_S

    def test_a_huge_failure_count_neither_overflows_nor_exceeds_the_ceiling(self) -> None:
        assert km._backoff_delay_s(10**9, lambda: 1.0) == km._REFRESH_RETRY_MAX_DELAY_S

    def test_the_constants_keep_their_documented_relationship(self) -> None:
        assert km._REFRESH_RETRY_BASE_DELAY_S > km._MIN_REFRESH_DELAY_S
        assert km._REFRESH_RETRY_BASE_DELAY_S * 2**km._MAX_REFRESH_RETRY_EXPONENT >= km._REFRESH_RETRY_MAX_DELAY_S
        # The lock is held for one HTTP call; it must stay well under the leeway the token has left.
        assert km._HTTP_TIMEOUT_S < km._EXPIRY_LEEWAY_S


class TestTheBackgroundLoopSurvivesEveryFailure:
    """A failed refresh must never end proactive refresh for the process's lifetime."""

    def test_a_refused_refresh_is_retried_and_the_provider_recovers(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1"), refused(), token("acc-3")])
        event: ScriptedEvent = ScriptedEvent([False, False], clock)
        provider: KeycloakTokenProvider = build(transport, clock, event)

        run_loop(provider, event, clock)

        assert transport.grants() == ["password", "refresh_token", "refresh_token"]
        assert provider.access_token == "acc-3"
        assert provider._consecutive_refresh_failures == 0

    @pytest.mark.parametrize(
        "failure",
        [
            OSError("network unreachable"),
            requests.ConnectionError("connection refused"),
            requests.Timeout("read timed out"),
            RuntimeError("a bug in a custom transport"),
            refused(503, {"error": "temporarily_unavailable"}),
            refused(502, None),
            FakeResponse(200, ValueError("Expecting value"), text="<html>bad gateway</html>"),
            FakeResponse(200, ["not", "an", "object"]),
            FakeResponse(200, {"expires_in": 300}),
            FakeResponse(200, {"access_token": "acc", "expires_in": "soon"}),
        ],
        ids=[
            "oserror",
            "connection-error",
            "timeout",
            "runtime-error",
            "503",
            "502",
            "non-json-200",
            "json-list",
            "no-access-token",
            "bad-expires-in",
        ],
    )
    def test_no_kind_of_failure_ends_the_loop(self, failure: Step) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1"), failure, token("acc-ok")])
        event: ScriptedEvent = ScriptedEvent([False, False], clock)
        provider: KeycloakTokenProvider = build(transport, clock, event)

        run_loop(provider, event, clock)

        assert len(transport.calls) == 3, "the loop stopped at the failure"
        assert provider.access_token == "acc-ok"

    def test_a_persistent_failure_keeps_the_loop_alive_without_repairing_the_provider(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1"), refused()])
        event: ScriptedEvent = ScriptedEvent([False] * 6, clock)
        provider: KeycloakTokenProvider = build(transport, clock, event)

        run_loop(provider, event, clock)

        assert transport.grants() == ["password"] + ["refresh_token"] * 6
        assert provider.access_token == "acc-1"
        assert provider._consecutive_refresh_failures == 6

    def test_no_failure_is_ever_answered_with_a_password_grant(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1"), refused(401, {"error": "invalid_client"})])
        event: ScriptedEvent = ScriptedEvent([False] * 10, clock)
        provider: KeycloakTokenProvider = build(transport, clock, event)

        run_loop(provider, event, clock)

        assert transport.grants().count("password") == 1, "the loop fell back to a password grant"


class TestTheBackgroundLoopBacksOff:
    """The retry cadence after a failure is the jittered ladder, never the 1 s scheduling floor."""

    def test_the_first_retry_waits_the_base_not_the_floor(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1"), refused(503), token("acc-2")])
        event: ScriptedEvent = ScriptedEvent([False, False], clock)
        provider: KeycloakTokenProvider = build(transport, clock, event)

        run_loop(provider, event, clock)

        assert event.wait_delays[0] == 300.0 - km._EXPIRY_LEEWAY_S
        assert event.wait_delays[1] == km._REFRESH_RETRY_BASE_DELAY_S

    def test_consecutive_failures_climb_the_ladder_to_the_ceiling(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1"), refused(503)])
        event: ScriptedEvent = ScriptedEvent([False] * 9, clock)
        provider: KeycloakTokenProvider = build(transport, clock, event, jitter=1.0)

        run_loop(provider, event, clock)

        assert event.wait_delays[1:] == [5.0, 10.0, 20.0, 40.0, 80.0, 160.0, 300.0, 300.0, 300.0]

    def test_a_success_resets_the_ladder_to_the_healthy_schedule(self, records: List[str]) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport(
            [token("acc-1"), refused(503), refused(503), token("acc-4", 120), refused(503)]
        )
        event: ScriptedEvent = ScriptedEvent([False] * 4, clock)
        provider: KeycloakTokenProvider = build(transport, clock, event, jitter=1.0)

        run_loop(provider, event, clock)

        # 270 healthy, 5 and 10 backing off, 90 healthy again from the NEW expiry, then 5: the ladder
        # restarted at the bottom instead of continuing at 20.
        assert event.wait_delays == [270.0, 5.0, 10.0, 90.0, 5.0]
        assert sum("recovered after 2 failed attempt(s)" in record for record in records) == 1

    def test_the_backoff_is_measured_from_when_the_failure_was_recorded(self) -> None:
        """An attempt that hangs must not schedule a retry that is already due when it returns."""
        clock: Dict[str, float] = {"now": 1000.0}

        class HangingTransport(FakeTransport):
            def post(self, url: str, data: Dict[str, str], timeout: float) -> FakeResponse:
                if data.get("grant_type") == "refresh_token":
                    clock["now"] += km._HTTP_TIMEOUT_S
                return super().post(url, data, timeout)

        transport: HangingTransport = HangingTransport([token("acc-1"), refused(503)])
        event: ScriptedEvent = ScriptedEvent([False, False], clock)
        provider: KeycloakTokenProvider = build(transport, clock, event)

        run_loop(provider, event, clock)

        assert event.wait_delays[1] == km._REFRESH_RETRY_BASE_DELAY_S

    def test_the_login_deadline_still_ends_the_loop_while_it_backs_off(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1", 30), refused(503)])
        event: ScriptedEvent = ScriptedEvent([False] * 50, clock)
        provider: KeycloakTokenProvider = build(transport, clock, event, jitter=1.0, token_expiration_in_s=100)

        run_loop(provider, event, clock)

        assert clock["now"] <= 1000.0 + 100.0 + km._MIN_REFRESH_DELAY_S
        assert event.is_set(), "the loop did not stop at the deadline"
        assert all(delay <= 100.0 for delay in event.wait_delays)

    def test_stop_during_a_backoff_wait_ends_the_loop_without_another_request(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1"), refused(503)])
        event: ScriptedEvent = ScriptedEvent([False, True], clock, advance_by=[270.0, 1.0])
        provider: KeycloakTokenProvider = build(transport, clock, event)

        run_loop(provider, event, clock)

        assert transport.grants() == ["password", "refresh_token"]

    def test_a_collected_provider_ends_the_loop(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        event: ScriptedEvent = ScriptedEvent([False] * 3, clock)
        provider: KeycloakTokenProvider = build(FakeTransport([token("acc-1")]), clock, event)
        reference: "weakref.ref[KeycloakTokenProvider]" = weakref.ref(provider)
        del provider

        km._refresh_loop(reference, event, lambda: clock["now"])  # type: ignore[arg-type]

        assert reference() is None


class TestTheLazyPathHonoursTheBackoff:
    """``authorization_metadata`` (called by every gRPC call) shares the loop's failure state."""

    def test_a_still_valid_token_is_served_when_its_refresh_fails(self, records: List[str]) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1", 300), refused(503)])
        provider: KeycloakTokenProvider = build(transport, clock)

        clock["now"] += 300.0 - km._EXPIRY_LEEWAY_S + 1.0  # inside the leeway, 29 s still valid

        assert provider.authorization_metadata() == ("authorization", "Bearer acc-1")
        assert any(record.startswith("WARNING") and "refresh failed (attempt 1)" in record for record in records)

    def test_no_request_is_sent_while_the_backoff_runs(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1", 300), refused(503)])
        provider: KeycloakTokenProvider = build(transport, clock)
        clock["now"] += 275.0

        for _ in range(100):
            provider.authorization_metadata()
            clock["now"] += 0.04  # 4 s of calls, all inside the 5 s backoff

        assert transport.grants() == ["password", "refresh_token"], "every call hit the token endpoint"

    def test_an_expired_token_raises_during_the_backoff_without_a_request(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1", 300), refused(503)])
        provider: KeycloakTokenProvider = build(transport, clock, jitter=1.0)
        clock["now"] += 299.0
        provider.authorization_metadata()  # fails, backs off 5 s, token valid 1 s more
        clock["now"] += 2.0  # expired, backoff still running

        with pytest.raises(KeycloakAuthenticationError, match="backing off after 1 consecutive failure"):
            provider.authorization_metadata()
        assert len(transport.calls) == 2

    def test_an_expired_token_whose_refresh_fails_raises(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1", 300), refused()])
        provider: KeycloakTokenProvider = build(transport, clock)
        clock["now"] += 400.0

        with pytest.raises(KeycloakAuthenticationError, match="status 400"):
            provider.authorization_metadata()

    def test_a_non_keycloak_exception_reaches_the_caller_as_a_keycloak_error(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1", 300), RuntimeError("transport bug")])
        provider: KeycloakTokenProvider = build(transport, clock)
        clock["now"] += 400.0

        with pytest.raises(KeycloakAuthenticationError) as raised:
            provider.authorization_metadata()
        assert isinstance(raised.value.__cause__, RuntimeError)

    def test_the_lazy_path_retries_once_the_backoff_elapses_and_recovers(self, records: List[str]) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1", 300), refused(503), token("acc-3", 300)])
        provider: KeycloakTokenProvider = build(transport, clock)
        clock["now"] += 280.0
        provider.authorization_metadata()
        clock["now"] += km._REFRESH_RETRY_BASE_DELAY_S

        assert provider.authorization_metadata() == ("authorization", "Bearer acc-3")
        assert provider._consecutive_refresh_failures == 0
        assert any(record.startswith("INFO") and "recovered after 1 failed attempt" in record for record in records)

    def test_a_lazy_failure_schedules_the_background_loops_next_wake(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport([token("acc-1", 300), refused(503), token("acc-3", 300)])
        event: ScriptedEvent = ScriptedEvent([False], clock)
        provider: KeycloakTokenProvider = build(transport, clock, event, jitter=1.0)
        clock["now"] += 280.0
        provider.authorization_metadata()  # backoff: next attempt at +5 s
        clock["now"] += 2.0

        run_loop(provider, event, clock)

        assert event.wait_delays[0] == pytest.approx(3.0), "the loop ignored the lazy path's backoff"
        assert provider.access_token == "acc-3"

    def test_concurrent_calls_during_an_outage_send_one_request_and_never_raise(self) -> None:
        """16 threads hammering a provider whose token is inside the leeway while Keycloak is down."""
        transport: FakeTransport = FakeTransport([token("acc-1", 20), OSError("down")], delay_s=0.05)
        provider: KeycloakTokenProvider = KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
            transport=transport,  # type: ignore[arg-type]
            start_background_refresh=False,
        )
        errors: List[BaseException] = []
        values: List[str] = []

        def call() -> None:
            for _ in range(20):
                try:
                    values.append(provider.authorization_metadata()[1])
                except BaseException as exception:  # noqa: BLE001 - collected for the assertion
                    errors.append(exception)

        threads: List[threading.Thread] = [threading.Thread(target=call) for _ in range(16)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=30.0)

        assert not errors, f"calls failed while the token was still valid: {errors[:2]}"
        assert set(values) == {"Bearer acc-1"} and len(values) == 320
        assert transport.grants() == ["password", "refresh_token"]


class TestTheTokenEndpointAnswerIsValidated:
    """Every way the exchange can fail is one ``KeycloakAuthenticationError``; no partial state."""

    @pytest.mark.parametrize(
        "failure",
        [OSError("unreachable"), requests.ConnectionError("refused"), requests.Timeout("timed out")],
        ids=["oserror", "connection-error", "timeout"],
    )
    def test_a_network_failure_at_login_is_a_keycloak_error_with_its_cause(self, failure: BaseException) -> None:
        with pytest.raises(KeycloakAuthenticationError, match="could not reach the token endpoint") as raised:
            build(FakeTransport([failure]), {"now": 0.0})
        assert raised.value.__cause__ is failure

    def test_a_non_json_body_is_a_keycloak_error(self) -> None:
        with pytest.raises(KeycloakAuthenticationError, match="not JSON"):
            build(FakeTransport([FakeResponse(200, ValueError("Expecting value"))]), {"now": 0.0})

    def test_a_json_body_that_is_not_an_object_is_a_keycloak_error(self) -> None:
        with pytest.raises(KeycloakAuthenticationError, match="JSON list"):
            build(FakeTransport([FakeResponse(200, ["access_token"])]), {"now": 0.0})

    def test_a_huge_error_page_is_truncated_in_the_message(self) -> None:
        page: str = "<html>" + "x" * 10_000 + "</html>"
        with pytest.raises(KeycloakAuthenticationError) as raised:
            build(FakeTransport([FakeResponse(502, None, text=page)]), {"now": 0.0})
        assert len(str(raised.value)) < km._MAX_ERROR_BODY_CHARS + 200

    def test_a_response_without_an_access_token_names_fields_never_values(self) -> None:
        body: Dict[str, Any] = {"refresh_token": "secret-offline-token-77", "expires_in": 300}
        with pytest.raises(KeycloakAuthenticationError) as raised:
            build(FakeTransport([FakeResponse(200, body)]), {"now": 0.0})
        assert "refresh_token" in str(raised.value)
        assert "secret-offline-token-77" not in str(raised.value)

    def test_a_non_numeric_expires_in_leaves_the_previous_token_untouched(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport(
            [token("acc-1", 300), FakeResponse(200, {"access_token": "acc-bad", "expires_in": "soon"})]
        )
        provider: KeycloakTokenProvider = build(transport, clock)
        clock["now"] += 280.0

        provider.authorization_metadata()

        assert provider.access_token == "acc-1"
        assert provider._access_token_expires_at == 1300.0

    def test_a_numeric_string_expires_in_is_accepted(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        provider: KeycloakTokenProvider = build(FakeTransport([token("acc-1", "300")]), clock)
        assert provider._access_token_expires_at == 1300.0

    def test_a_negative_expires_in_counts_as_already_expired(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        provider: KeycloakTokenProvider = build(FakeTransport([token("acc-1", -50)]), clock)
        assert provider._access_token_expires_at == 1000.0

    def test_a_refresh_without_a_new_refresh_token_keeps_the_previous_one(self) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport(
            [token("acc-1", 300, refresh="off-1"), token("acc-2", 300, refresh=None), token("acc-3", 300)]
        )
        provider: KeycloakTokenProvider = build(transport, clock)
        clock["now"] += 280.0
        provider.authorization_metadata()
        clock["now"] += 280.0
        provider.authorization_metadata()

        assert [call.get("refresh_token") for call in transport.calls[1:]] == ["off-1", "off-1"]


class TestNoCredentialReachesALog:
    """Failure logging names the failure, never a password, refresh token or access token."""

    def test_the_failure_lines_carry_no_credential(self, records: List[str]) -> None:
        clock: Dict[str, float] = {"now": 1000.0}
        transport: FakeTransport = FakeTransport(
            [token("acc-secret-1", 300, refresh="off-secret-1"), refused(503), token("acc-secret-2", 300)]
        )
        event: ScriptedEvent = ScriptedEvent([False, False], clock)
        provider: KeycloakTokenProvider = build(transport, clock, event)

        run_loop(provider, event, clock)

        rendered: str = "\n".join(records)
        assert "refresh failed (attempt 1)" in rendered and "recovered" in rendered
        for secret in (PASSWORD, "acc-secret-1", "off-secret-1", "acc-secret-2"):
            assert secret not in rendered, f"{secret} reached a log line"


class TestStopIsSafeFromAnyState:
    """``stop`` is idempotent, bounded and quiet, including during interpreter finalization."""

    def test_stop_is_idempotent_and_safe_without_a_thread(self) -> None:
        provider: KeycloakTokenProvider = build(FakeTransport([token("acc-1")]), {"now": 0.0})
        provider.stop()
        provider.stop()

    def test_stop_skips_the_join_once_the_interpreter_is_finalizing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        provider: KeycloakTokenProvider = build(FakeTransport([token("acc-1")]), {"now": 0.0})
        joined: List[bool] = []
        provider._refresh_thread = types.SimpleNamespace(join=lambda timeout: joined.append(True))  # type: ignore[assignment]
        monkeypatch.setattr(km.sys, "is_finalizing", lambda: True)

        provider.stop()

        assert not joined

    def test_a_join_refused_by_finalization_does_not_escape(self) -> None:
        provider: KeycloakTokenProvider = build(FakeTransport([token("acc-1")]), {"now": 0.0})

        def refuse(timeout: float) -> None:
            raise RuntimeError("cannot join thread at interpreter shutdown")

        provider._refresh_thread = types.SimpleNamespace(join=refuse)  # type: ignore[assignment]
        provider.stop()


class TestTheRealThreadRecovers:
    """End to end on a real daemon thread and the real clock, with the timings shrunk."""

    def test_the_thread_survives_failures_and_the_token_recovers(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(km, "_EXPIRY_LEEWAY_S", 0.05)
        monkeypatch.setattr(km, "_MIN_REFRESH_DELAY_S", 0.01)
        monkeypatch.setattr(km, "_REFRESH_RETRY_BASE_DELAY_S", 0.05)
        monkeypatch.setattr(km, "_REFRESH_RETRY_MAX_DELAY_S", 0.05)
        transport: FakeTransport = FakeTransport(
            [token("acc-1", 0.1), OSError("down"), refused(503), RuntimeError("bug"), token("acc-ok", 3600)]
        )
        provider: KeycloakTokenProvider = KeycloakTokenProvider(
            keycloak_url=KEYCLOAK_URL,
            realm=REALM,
            client_id=CLIENT_ID,
            username=USERNAME,
            password=PASSWORD,
            transport=transport,  # type: ignore[arg-type]
        )
        try:
            deadline: float = time.monotonic() + 10.0
            while provider.access_token != "acc-ok" and time.monotonic() < deadline:
                time.sleep(0.01)

            assert provider.access_token == "acc-ok", f"no recovery; grants so far: {transport.grants()}"
            thread: Optional[threading.Thread] = provider._refresh_thread
            assert thread is not None and thread.is_alive(), "the refresh thread died"
            assert transport.grants() == ["password"] + ["refresh_token"] * 4
        finally:
            provider.stop()
        assert provider._refresh_thread is not None and not provider._refresh_thread.is_alive()


class TestTheProviderRegistryIsKeyedByCredentials:
    """Two clients share a provider exactly when they authenticate as the same identity."""

    @staticmethod
    def config(**overrides: Any) -> Any:
        fields: Dict[str, Any] = {
            "keycloak_url": KEYCLOAK_URL,
            "realm": REALM,
            "client_id": CLIENT_ID,
            "user_name": USERNAME,
            "password": PASSWORD,
            "token_expiration_in_s": None,
            "keycloak_verify_ssl": True,
            "refresh_token": "",
        }
        fields.update(overrides)
        # The SDKs spell the user name three ways (``user_name``, ``username``, ``resolved_username``)
        # and two of them gate on a "configured" flag; carry every spelling, kept in step.
        fields["username"] = fields["resolved_username"] = fields["user_name"]
        fields["is_keycloak_auth_configured"] = fields["keycloak_configured"] = True
        return types.SimpleNamespace(**fields)

    @pytest.fixture
    def built(self, monkeypatch: pytest.MonkeyPatch) -> List[Dict[str, Any]]:
        constructed: List[Dict[str, Any]] = []

        class Recorder:
            def __init__(self, **kwargs: Any) -> None:
                constructed.append(kwargs)

        monkeypatch.setattr(km, "KeycloakTokenProvider", Recorder)
        monkeypatch.setattr(km, "_PROVIDER_REGISTRY", weakref.WeakValueDictionary())
        return constructed

    def test_the_same_credentials_share_one_provider(self, built: List[Dict[str, Any]]) -> None:
        first: Any = km.get_keycloak_token_provider(self.config())
        second: Any = km.get_keycloak_token_provider(self.config())
        assert first is second and len(built) == 1

    @pytest.mark.parametrize(
        "field, value",
        [("user_name", "other@example.com"), ("password", "other-pw"), ("realm", "other"), ("keycloak_url", "x")],
    )
    def test_different_credentials_never_share_a_provider(
        self, built: List[Dict[str, Any]], field: str, value: str
    ) -> None:
        first: Any = km.get_keycloak_token_provider(self.config())
        second: Any = km.get_keycloak_token_provider(self.config(**{field: value}))
        assert first is not second

    def test_a_freed_config_whose_address_is_reused_never_hands_over_its_provider(
        self, built: List[Dict[str, Any]]
    ) -> None:
        keep: List[Any] = []
        for index in range(50):
            # The config dies right after the call, so CPython is free to reuse its address.
            keep.append(km.get_keycloak_token_provider(self.config(user_name=f"user-{index}@example.com")))
        assert [kwargs["username"] for kwargs in built] == [f"user-{index}@example.com" for index in range(50)]

    def test_the_registry_key_does_not_contain_the_password(self) -> None:
        key: str = km._provider_registry_key(self.config())
        assert PASSWORD not in key and len(key) == 64
