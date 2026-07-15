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
import math
import threading
from queue import (
    Empty,
    Full,
    Queue,
)

from loguru import logger
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.nlu.client import Client


class ClientPool:
    def __init__(
        self,
        config: BaseClientConfig,
        use_secure_channel: bool = True,
        pool_size: int = 10,
        max_size_ratio: float = 1.5,
    ) -> None:
        """
        Initialise a ClientPool to handle all your requests.

        Args:
            config: Client configuration; the same will be used on all clients created in the pool
            use_secure_channel: self-explanatory
            pool_size: self-explanatory
            max_size_ratio: this is: (maximum_pool_size / pool_size); the pool can grow to up to a limit

        Raises:
            ValueError:
                If `max_size_ratio` is small enough that the resulting maximum pool size cannot even
                hold the `pool_size` clients the pool is pre-filled with.
        """
        # Client configuration
        self.config: BaseClientConfig = config
        self.use_secure_channel: bool = use_secure_channel

        # Queue control mechanism
        self.pool_size: int = pool_size
        self.max_size_ratio: float = max_size_ratio
        self.max_size: int = math.floor(self.pool_size * self.max_size_ratio)

        # `_initialize_pool` puts `pool_size` clients into a queue bounded by `max_size`. If `max_size`
        # is the smaller of the two, that put blocks forever on a queue that can never drain -- fail
        # fast here instead of hanging the caller's process.
        if self.max_size < self.pool_size:
            raise ValueError(
                "`max_size_ratio` must be at least 1.0: the pool is pre-filled with `pool_size` clients, "
                "so a maximum pool size below that can never be filled.\n"
                f"\t - pool_size: {self.pool_size}\n"
                f"\t - max_size_ratio: {self.max_size_ratio}\n"
                f"\t - resulting max_size: floor({self.pool_size} * {self.max_size_ratio}) = {self.max_size}."
            )

        # Mechanism to prevent unlimited creation of clients
        self.n_clients_created_limit: int = math.ceil(self.max_size * 1.5)
        self.n_clients_created: int = 0
        # The `Queue` is thread-safe, but `n_clients_created` is not. In `acquire_client` the limit check
        # and the increment that follows it must be a single atomic step, otherwise two threads that
        # overflow concurrently read the same value, both pass the check and both create a client -- so the
        # counter lost-updates and `n_clients_created_limit` is exceeded. `_initialize_pool` needs no lock:
        # it runs from `__init__`, before this object can be shared with another thread.
        self._creation_lock: threading.Lock = threading.Lock()

        # initialization
        self.pool: Queue[Client] = Queue(maxsize=self.max_size)
        self._initialize_pool()

    def _initialize_pool(self) -> None:
        for i in range(self.pool_size):
            self.pool.put(Client(config=self.config, use_secure_channel=self.use_secure_channel))
            self.n_clients_created += 1

    def acquire_client(self) -> Client:
        try:
            return self.pool.get(block=True, timeout=2)
        except Empty:
            logger.warning(
                "The ClientPool is empty, cannot retrieve more clients from it.\n"
                "Opening new client to fulfill request..."
            )

            with self._creation_lock:
                if self.n_clients_created_limit <= self.n_clients_created:
                    raise Full(
                        'A concerning number of "Clients" have been created.'
                        'Remember to "release" (or "disconnect) the clients after using them.\n'
                        "If there are too many requests, consider increasing the pool size.\n"
                        f"\t - # clients created: {self.n_clients_created}\n"
                        f"\t - Current max pool size: {self.max_size}."
                    )

                self.n_clients_created += 1

            # Built outside the critical section: constructing a `Client` opens gRPC channels and must
            # not serialise every other thread's limit check behind it.
            return Client(config=self.config, use_secure_channel=self.use_secure_channel)

    def release_client(self, c: Client) -> None:
        # `put_nowait` (and not `put`, which defaults to `block=True, timeout=None`) is what makes the
        # `except Full` branch reachable: a blocking put would wait for a free slot forever, deadlocking
        # the caller instead of closing the surplus client.
        try:
            self.pool.put_nowait(c)
        except Full:
            logger.warning(
                "The ClientPool is full, putting more clients into it is not possible.\nClosing client connection..."
            )
            c.disconnect()

    def close(self) -> None:
        while not self.pool.empty():
            c: Client = self.pool.get()
            c.disconnect()
