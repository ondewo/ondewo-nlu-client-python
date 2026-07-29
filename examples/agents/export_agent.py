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

from ondewo.nlu.agent_pb2 import (
    ExportAgentRequest,
    ExportAgentResponse,
)
from ondewo.nlu.client import Client

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from example_env import (  # noqa: E402
    env,
    get_client_config,
    use_secure_channel,
)
from ondewo.nlu.operations_pb2 import (  # noqa: E402
    GetOperationRequest,
    Operation,
)

if __name__ == "__main__":
    # All settings come from examples/environment.env — see examples/example_env.py.
    parent: str = env("ONDEWO_NLU_CAI_AGENT_PARENT")

    client: Client = Client(config=get_client_config(), use_secure_channel=use_secure_channel())
    export_operation: Operation = client.services.agents.export_agent(ExportAgentRequest(parent=parent))

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

    with open(env("ONDEWO_NLU_CAI_AGENT_ZIP_PATH"), mode="wb") as zf:
        zf.write(export_response.agent_content)
