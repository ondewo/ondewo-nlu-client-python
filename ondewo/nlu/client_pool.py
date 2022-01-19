# Copyright 2021 ONDEWO GmbH
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
from queue import Queue, Full, Empty

from ondewo.logging.logger import logger
from ondewo.utils.base_client_config import BaseClientConfig

from ondewo.nlu.client import Client


class ClientPool:
    def __init__(
            self,
            config: BaseClientConfig,
            use_secure_channel: bool = True,
            pool_size: int = 10,
            max_size_ratio: float = 1.5
    ) -> None:
        """
        Initialise a ClientPool to handle all your requests.

        Args:
            config: Client configuration; the same will be used on all clients created in the pool
            use_secure_channel: self-explanatory
            pool_size: self-explanatory
            max_size_ratio: this is: (maximum_pool_size / pool_size); the pool can grow to up to a limit
        """
        # Client configuration
        self.config: BaseClientConfig = config
        self.use_secure_channel: bool = use_secure_channel

        # Queue control mechanism
        self.pool_size: int = pool_size
        self.max_size_ratio: float = max_size_ratio
        self.max_size: int = math.floor(self.pool_size * self.max_size_ratio)

        # Mechanism to prevent unlimited creation of clients
        self.n_clients_created_limit: int = math.ceil(self.max_size * 1.5)
        self.n_clients_created: int = 0

        # initialization
        self.pool: Queue = Queue(maxsize=self.max_size)
        self._initialize_pool()

    def _initialize_pool(self) -> None:
        for i in range(self.pool_size):
            self.pool.put(Client(config=self.config, use_secure_channel=self.use_secure_channel))
            self.n_clients_created += 1

    def acquire_client(self) -> Client:
        try:
            return self.pool.get(block=True, timeout=2)
        except Empty:
            logger.warning(f'The ClientPool is empty, cannot retrieve more clients from it.\n'
                           f'Opening new client to fulfill request...')

            if self.n_clients_created_limit <= self.n_clients_created:
                raise Full(f'A concerning number of "Clients" have been created.'
                           f'Remember to "release" (or "disconnect) the clients after using them.\n'
                           f'If there are too many requests, consider increasing the pool size.\n'
                           f'\t - # clients created: {self.n_clients_created}\n'
                           f'\t - Current max pool size: {self.max_size}.')

            self.n_clients_created += 1
            return Client(config=self.config, use_secure_channel=self.use_secure_channel)

    def release_client(self, c: Client) -> None:
        try:
            self.pool.put(c)
        except Full:
            logger.warning(f'The ClientPool is full, putting more clients into it is not possible.\n'
                           f'Closing client connection...')
            c.disconnect()

    def close(self) -> None:
        while not self.pool.empty():
            c: Client = self.pool.get()
            c.disconnect()
