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
from typing import Optional

import polling

from ondewo.nlu.agent_pb2 import RestoreAgentRequest
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.operations_pb2 import (
    GetOperationRequest,
    Operation,
)

if __name__ == '__main__':
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    zip_path: str = '<the path of your zip file>'
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )

    client: Client = Client(config=config, use_secure_channel=False)

    with open(zip_path, 'rb') as file:
        byte_object = file.read()

    restore_operation: Operation = client.services.agents.restore_agent(
        RestoreAgentRequest(parent=parent, agent_content=byte_object)
    )

    polling.poll(
        target=client.services.operations.get_operation,
        step=1,
        args=(GetOperationRequest(name=restore_operation.name),),
        check_success=lambda op: op.done,
        timeout=600,  # wait 10 minutes until training is finished
    )

    op: Optional[Operation] = \
        client.services.operations.get_operation(GetOperationRequest(name=restore_operation.name))
    assert op
    assert op.done
