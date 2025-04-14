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
import json
from typing import Optional

import polling

from ondewo.nlu.agent_pb2 import (
    ExportAgentRequest,
    ExportAgentResponse,
)
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.operations_pb2 import (
    GetOperationRequest,
    Operation,
)

if __name__ == '__main__':
    parent: str = 'projects/some_agent_id/agent'
    config_file: str = 'envs/example.json'

    with open(config_file) as f:
        config_ = json.load(f)

    config = ClientConfig(
        host=config_['host'],
        port=config_['port'],
        user_name=config_['user_name'],
        password=config_['password'],
        http_token=config_['http_token'],
        grpc_cert=config_.get('grpc_cert', '').encode().decode().replace('\\n', '\n'),  # type: ignore
    )

    client: Client = Client(config=config, use_secure_channel=True)
    export_operation: Operation = client.services.agents.export_agent(
        ExportAgentRequest(
            parent=parent
        )
    )

    polling.poll(
        target=client.services.operations.get_operation,
        step=1,
        args=(GetOperationRequest(name=export_operation.name),),
        check_success=lambda op: op.done,
        timeout=600,  # wait 10 minutes until training is finished
    )

    export_operation_update: Optional[Operation] = client.services.operations.get_operation(
        GetOperationRequest(name=export_operation.name)
    )
    export_response: ExportAgentResponse = ExportAgentResponse()
    if export_operation_update is not None:
        export_operation_update.response.Unpack(export_response)
        assert export_response.agent_content
    else:
        assert False

    with open('my_backup.zip', mode='wb') as zf:
        zf.write(export_response.agent_content)
