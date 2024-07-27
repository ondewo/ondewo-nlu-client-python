# Copyright 2021-2024 ONDEWO GmbH
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
from typing import Optional

import polling

from ondewo.nlu.agent_pb2 import TrainAgentRequest
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.operations_pb2 import (
    GetOperationRequest,
    Operation,
)

if __name__ == '__main__':
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )

    client: Client = Client(config=config, use_secure_channel=True)

    train_operation: Operation = client.services.agents.train_agent(
        TrainAgentRequest(
            parent=parent
        )
    )

    polling.poll(
        target=client.services.operations.get_operation,
        step=1,
        args=(GetOperationRequest(name=train_operation.name),),
        check_success=lambda op: op.done,
        timeout=60 * 60 * 1,  # wait 1 hour until training is finished
    )

    training_operation_update: Optional[Operation] = client.services.operations.get_operation(
        GetOperationRequest(name=train_operation.name)
    )
    if training_operation_update is not None:
        assert training_operation_update.done
