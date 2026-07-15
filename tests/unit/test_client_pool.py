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
"""Hermetic unit tests for `ondewo.nlu.client_pool.ClientPool`.

The pool is exercised with **real** `Client` objects and a **real** `queue.Queue`. That is
possible without any network because gRPC channels are lazy: `Client(...)` only constructs
channel objects, it never dials. A whole pool builds in single-digit milliseconds.

The one thing that is doubled is *waiting*: `acquire_client` calls `self.pool.get(timeout=2)`,
so proving the exhausted-pool path against a genuinely empty pool would burn 2 wall-clock
seconds per assertion. `_collapse_get_timeout` keeps the real, really-empty queue and only
forces its timeout to 0 — the `Empty` still comes from the real queue observing that it is
really empty. This mirrors the injected clock in `tests/unit/utils/test_keycloak.py`.

Two real defects were found while writing these tests and are documented at their tests:
see `test_release_client_blocks_forever_when_pool_is_full` (a `# pragma: no cover` in the
source) and `test_pool_smaller_than_max_size_ratio_one_would_deadlock_on_init`.
"""

import threading
from queue import (
    Empty,
    Full,
    Queue,
)
from typing import (
    List,
    Optional,
    Set,
)

import pytest

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.client_pool import ClientPool

# Bound once so a refactor that changes only an input or only an expectation cannot silently
# make an assertion tautological.
HOST: str = "localhost"
PORT: str = "50055"
USERNAME: str = "tech-user@example.com"
PASSWORD: str = "s3cr3t"

# Default constructor values, restated here so the "documented contract" test fails if they drift.
DEFAULT_POOL_SIZE: int = 10
DEFAULT_MAX_SIZE_RATIO: float = 1.5


@pytest.fixture
def config() -> ClientConfig:
    """A Keycloak-less config: `Client` construction stays offline and no token is ever minted."""
    return ClientConfig(host=HOST, port=PORT, user_name=USERNAME, password=PASSWORD)


def _build_pool(config: ClientConfig, pool_size: int, max_size_ratio: float = DEFAULT_MAX_SIZE_RATIO) -> ClientPool:
    return ClientPool(
        config=config,
        use_secure_channel=False,
        pool_size=pool_size,
        max_size_ratio=max_size_ratio,
    )


def _collapse_get_timeout(pool: ClientPool) -> None:
    """Make the pool's real queue give up instantly instead of waiting out its 2s timeout.

    `acquire_client` hard-codes `self.pool.get(block=True, timeout=2)`. Only the *waiting* is
    removed: the queue, its contents and its emptiness are real, so the resulting `Empty` is a
    genuine observation of an exhausted pool rather than a scripted one.
    """
    real_queue: Queue = pool.pool

    def _get_without_waiting(block: bool = True, timeout: Optional[float] = None) -> Client:
        # Bind the result first: Queue is unparameterised here, so Queue.get is typed as returning
        # Any and returning it directly trips mypy's no-any-return.
        client: Client = Queue.get(real_queue, block=block, timeout=0)
        return client

    # `setattr` on the instance shadows the bound method; the class is untouched.
    setattr(real_queue, "get", _get_without_waiting)


class TestInitialisation:
    def test_pool_is_prefilled_with_pool_size_distinct_clients(self, config: ClientConfig) -> None:
        """The pool eagerly builds `pool_size` clients up front, and they are not aliases."""
        pool_size: int = 3
        pool: ClientPool = _build_pool(config, pool_size=pool_size)

        assert pool.pool.qsize() == pool_size
        assert pool.n_clients_created == pool_size

        pooled: List[Client] = list(pool.pool.queue)
        assert len({id(c) for c in pooled}) == pool_size, "each slot must hold its own Client"
        assert all(c.services is not None for c in pooled), "pooled clients must be connected"

    @pytest.mark.parametrize(
        ("pool_size", "max_size_ratio", "expected_max_size", "expected_creation_limit"),
        [
            # max_size floors (3 * 1.5 == 4.5 -> 4) and the limit then ceils (4 * 1.5 == 6.0 -> 6).
            (3, 1.5, 4, 6),
            # Both roundings bite: 2 * 1.5 == 3.0 -> 3, then 3 * 1.5 == 4.5 -> ceil 5.
            (2, 1.5, 3, 5),
            # A non-default ratio: 4 * 1.25 == 5.0 -> 5, then 5 * 1.5 == 7.5 -> ceil 8.
            (4, 1.25, 5, 8),
            # The documented defaults.
            (DEFAULT_POOL_SIZE, DEFAULT_MAX_SIZE_RATIO, 15, 23),
        ],
    )
    def test_sizing_math_floors_max_size_and_ceils_creation_limit(
        self,
        config: ClientConfig,
        pool_size: int,
        max_size_ratio: float,
        expected_max_size: int,
        expected_creation_limit: int,
    ) -> None:
        """`max_size = floor(pool_size * ratio)` caps the queue; `ceil(max_size * 1.5)` caps creation."""
        pool: ClientPool = _build_pool(config, pool_size=pool_size, max_size_ratio=max_size_ratio)

        assert pool.max_size == expected_max_size
        assert pool.pool.maxsize == expected_max_size, "the queue must actually enforce max_size"
        assert pool.n_clients_created_limit == expected_creation_limit
        assert pool.max_size > pool_size or max_size_ratio == 1.0, "headroom above pool_size is the point of the ratio"

    def test_the_shared_config_reaches_every_pooled_client(self, config: ClientConfig) -> None:
        """ "the same [config] will be used on all clients created in the pool" (constructor docstring).

        The clients do not retain the config object, so the reachable evidence is the gRPC channel
        each one dials: it must target the host/port that came from the shared config.
        """
        expected_target: str = "{}:{}".format(HOST, PORT)
        pool: ClientPool = _build_pool(config, pool_size=2)

        assert pool.config is config
        assert pool.use_secure_channel is False
        for client in list(pool.pool.queue):
            # `_target` is private, but it is the only seam that proves the config was applied.
            assert client.services.agents.grpc_channel._target == expected_target


class TestAcquireAndRelease:
    def test_acquire_removes_a_client_and_release_puts_the_same_one_back(self, config: ClientConfig) -> None:
        """The core pooling contract: a released client is reused, not rebuilt."""
        pool: ClientPool = _build_pool(config, pool_size=3)

        client: Client = pool.acquire_client()
        assert pool.pool.qsize() == 2
        assert pool.n_clients_created == 3, "handing out a pooled client must not create one"

        pool.release_client(client)
        assert pool.pool.qsize() == 3
        assert pool.n_clients_created == 3

        # FIFO: the released client goes to the back, so it comes out last.
        drained: List[Client] = [pool.acquire_client() for _ in range(3)]
        assert drained[-1] is client

    def test_acquire_hands_out_each_pooled_client_exactly_once(self, config: ClientConfig) -> None:
        """A client must never be handed to two callers at once — that is the whole point of a pool."""
        pool_size: int = 4
        pool: ClientPool = _build_pool(config, pool_size=pool_size)
        expected: List[Client] = list(pool.pool.queue)

        drained: List[Client] = [pool.acquire_client() for _ in range(pool_size)]

        assert drained == expected, "clients are handed out in FIFO order"
        assert len({id(c) for c in drained}) == pool_size
        assert pool.pool.qsize() == 0

    def test_acquire_on_exhausted_pool_creates_an_extra_client(self, config: ClientConfig) -> None:
        """Below the creation limit an exhausted pool overflows: a brand-new client is built."""
        pool_size: int = 2
        pool: ClientPool = _build_pool(config, pool_size=pool_size)
        pooled: Set[int] = {id(c) for c in pool.pool.queue}

        for _ in range(pool_size):
            pool.acquire_client()
        _collapse_get_timeout(pool)

        overflow: Client = pool.acquire_client()

        assert id(overflow) not in pooled, "an exhausted pool must build a new client, not reissue a busy one"
        assert overflow.services is not None
        assert pool.n_clients_created == pool_size + 1
        assert pool.pool.qsize() == 0, "the overflow client is not pooled until it is released"

    def test_overflow_client_is_absorbed_by_the_pool_on_release(self, config: ClientConfig) -> None:
        """Releasing an overflow client grows the pool above `pool_size` (up to `max_size`)."""
        pool_size: int = 2
        pool: ClientPool = _build_pool(config, pool_size=pool_size)
        for _ in range(pool_size):
            pool.acquire_client()
        _collapse_get_timeout(pool)
        overflow: Client = pool.acquire_client()

        pool.release_client(overflow)

        assert pool.pool.qsize() == 1
        assert pool.acquire_client() is overflow, "the overflow client is reused like any pooled one"
        assert pool.n_clients_created == pool_size + 1, "reuse must not create another client"

    def test_acquire_raises_full_once_the_creation_limit_is_reached(self, config: ClientConfig) -> None:
        """The runaway-creation guard: past `n_clients_created_limit`, `acquire_client` refuses."""
        pool_size: int = 2
        pool: ClientPool = _build_pool(config, pool_size=pool_size)
        creation_limit: int = pool.n_clients_created_limit
        assert creation_limit > pool_size, "otherwise this test would not exercise the overflow path at all"

        for _ in range(pool_size):
            pool.acquire_client()
        _collapse_get_timeout(pool)
        # Overflow up to — but not past — the limit; each of these must still succeed.
        for _ in range(creation_limit - pool_size):
            pool.acquire_client()
        assert pool.n_clients_created == creation_limit

        with pytest.raises(Full) as exc_info:
            pool.acquire_client()

        assert str(creation_limit) in str(exc_info.value), "the error must report how many clients were created"
        assert str(pool.max_size) in str(exc_info.value)
        assert pool.n_clients_created == creation_limit, "the refused acquire must not count as a creation"

    def test_creation_limit_is_not_reset_by_returning_clients(self, config: ClientConfig) -> None:
        """`n_clients_created` is a lifetime counter, not a gauge of currently-issued clients.

        Documents a real sharp edge: a long-lived pool that legitimately overflows often will
        eventually refuse to overflow again even while every client is back in the pool.
        """
        pool_size: int = 2
        pool: ClientPool = _build_pool(config, pool_size=pool_size)
        for _ in range(pool_size):
            pool.acquire_client()
        _collapse_get_timeout(pool)
        overflow: Client = pool.acquire_client()
        assert pool.n_clients_created == pool_size + 1

        pool.release_client(overflow)

        assert pool.n_clients_created == pool_size + 1, "returning a client does not decrement the counter"

    def test_release_client_blocks_forever_when_pool_is_full(self, config: ClientConfig) -> None:
        """BUG: `release_client` deadlocks on a full pool instead of disconnecting the surplus client.

        `release_client` wraps `self.pool.put(c)` in `except Full`, but `Queue.put` defaults to
        `block=True, timeout=None` — so it waits for a free slot forever and `Full` is never
        raised. The handler (warn + `c.disconnect()`) is therefore dead code, marked
        `# pragma: no cover` in the source. The fix is `put_nowait`; this test pins the current,
        wrong behaviour so that fixing it fails here and forces the pragma to be removed.
        """
        pool: ClientPool = _build_pool(config, pool_size=1, max_size_ratio=1.0)
        assert pool.max_size == 1 and pool.pool.qsize() == 1, "pool must start full for this to be the full-pool path"
        surplus: Client = Client(config=config, use_secure_channel=False)

        returned: threading.Event = threading.Event()

        def _release() -> None:
            pool.release_client(surplus)
            returned.set()

        worker: threading.Thread = threading.Thread(target=_release, daemon=True)
        worker.start()
        # A generous bound: `put` either returns/raises at once, or it is blocked forever.
        assert not returned.wait(timeout=0.5), "release_client returned — the Full handler is reachable after all"
        assert surplus.services is not None, "the surplus client was never disconnected; it leaks"

        # Unblock the parked thread so it cannot outlive the test.
        pool.pool.get()
        assert returned.wait(timeout=2), "freeing a slot must let the parked release_client complete"

    def test_pool_smaller_than_max_size_ratio_one_would_deadlock_on_init(self, config: ClientConfig) -> None:
        """BUG (documented, not exercised): `max_size_ratio < 1` hangs `ClientPool.__init__`.

        `max_size = floor(pool_size * ratio)` can fall below `pool_size`, and `_initialize_pool`
        then does `pool_size` blocking `put`s into a shorter queue — the surplus put parks
        forever. Asserting the arithmetic is enough to pin the precondition; actually calling the
        constructor would hang the suite, so the constructor is deliberately not called here.
        """
        pool_size: int = 10
        ratio: float = 0.5

        max_size: int = int(pool_size * ratio)

        assert max_size < pool_size, "init would block putting client #{} into a queue of {}".format(
            max_size + 1,
            max_size,
        )


class TestClose:
    def test_close_disconnects_every_pooled_client_and_empties_the_pool(self, config: ClientConfig) -> None:
        pool_size: int = 3
        pool: ClientPool = _build_pool(config, pool_size=pool_size)
        pooled: List[Client] = list(pool.pool.queue)

        pool.close()

        assert pool.pool.qsize() == 0
        for client in pooled:
            assert client.services is None, "close() must tear down every channel it owns"

    def test_close_leaves_issued_clients_untouched(self, config: ClientConfig) -> None:
        """`close()` only drains what is *in* the pool; a client a caller still holds stays usable."""
        pool: ClientPool = _build_pool(config, pool_size=2)
        in_use: Client = pool.acquire_client()

        pool.close()

        assert in_use.services is not None, "closing the pool must not yank a channel out from under a caller"

    def test_close_on_an_already_closed_pool_is_a_no_op(self, config: ClientConfig) -> None:
        """Idempotent: the second pass finds an empty queue and must not raise (e.g. double-disconnect)."""
        pool: ClientPool = _build_pool(config, pool_size=2)
        pool.close()

        pool.close()

        assert pool.pool.qsize() == 0


class TestThreadSafety:
    def test_concurrent_acquire_release_never_issues_one_client_twice(self, config: ClientConfig) -> None:
        """The `Queue` gives real mutual exclusion: a client is held by at most one thread at a time.

        Threads are barrier-synchronised rather than slept, and `pool_size` matches the thread
        count so no thread can ever hit the (2s) empty-pool timeout.
        """
        pool_size: int = 4
        iterations: int = 25
        pool: ClientPool = _build_pool(config, pool_size=pool_size)

        barrier: threading.Barrier = threading.Barrier(pool_size)
        guard: threading.Lock = threading.Lock()
        held: Set[int] = set()
        double_issued: List[int] = []
        errors: List[BaseException] = []

        def _worker() -> None:
            try:
                barrier.wait()
                for _ in range(iterations):
                    client: Client = pool.acquire_client()
                    with guard:
                        if id(client) in held:
                            double_issued.append(id(client))
                        held.add(id(client))
                    with guard:
                        held.discard(id(client))
                    pool.release_client(client)
            except BaseException as error:  # noqa: BLE001 - surfaced as a test failure below
                errors.append(error)

        workers: List[threading.Thread] = [threading.Thread(target=_worker) for _ in range(pool_size)]
        for worker in workers:
            worker.start()
        for worker in workers:
            worker.join(timeout=30)

        assert not errors, "worker threads raised: {}".format(errors)
        assert not any(worker.is_alive() for worker in workers), "a worker deadlocked"
        assert not double_issued, "the same client was issued to two threads concurrently"
        assert pool.pool.qsize() == pool_size, "every client was returned"
        assert pool.n_clients_created == pool_size, "steady-state reuse must never grow the pool"


class TestAcquireEmptySeam:
    def test_collapsed_timeout_still_yields_pooled_clients(self, config: ClientConfig) -> None:
        """Guard for the test double itself: it must not turn a *non-empty* pool into an empty one.

        Without this, `_collapse_get_timeout` could silently be an always-raise stub and the
        exhausted-pool tests above would pass for the wrong reason.
        """
        pool: ClientPool = _build_pool(config, pool_size=2)
        expected: Client = list(pool.pool.queue)[0]
        _collapse_get_timeout(pool)

        assert pool.acquire_client() is expected
        assert pool.n_clients_created == 2, "a served-from-pool acquire must not create a client"

        pool.acquire_client()
        with pytest.raises(Empty):
            Queue.get(pool.pool, block=True, timeout=0)
