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
import sys
from pathlib import Path
from typing import Optional

import polling

from ondewo.nlu.agent_pb2 import ImportAgentRequest
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.operations_pb2 import (
    GetOperationRequest,
    Operation,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from example_env import (  # noqa: E402
    env,
    get_client_config,
    use_secure_channel,
)

if __name__ == "__main__":
    parent: str = env("ONDEWO_NLU_CAI_AGENT_PARENT")
    zip_path: str = env("ONDEWO_NLU_CAI_AGENT_ZIP_PATH")
    config: ClientConfig = get_client_config()
    client: Client = Client(config=config, use_secure_channel=use_secure_channel())

    with open(zip_path, "rb") as file:
        byte_object = file.read()

    import_operation: Operation = client.services.agents.import_agent(
        ImportAgentRequest(parent=parent, agent_content=byte_object)
    )

    polling.poll(
        target=client.services.operations.get_operation,
        step=1,
        args=(GetOperationRequest(name=import_operation.name),),
        check_success=lambda op: op.done,
        timeout=600,  # wait 10 minutes until training is finished
    )

    operation: Optional[Operation] = client.services.operations.get_operation(
        GetOperationRequest(name=import_operation.name)
    )
    assert operation
    assert operation.done
