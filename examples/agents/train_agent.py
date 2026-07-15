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

from ondewo.nlu.agent_pb2 import TrainAgentRequest
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
    config: ClientConfig = get_client_config()

    client: Client = Client(config=config, use_secure_channel=use_secure_channel())

    train_operation: Operation = client.services.agents.train_agent(TrainAgentRequest(parent=parent))

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
        # `done` only means the operation finished — it is also set when training FAILED, and the
        # error is reported in `error` rather than raised. Without this check a failed training
        # looks exactly like a successful one, and the agent silently stays unable to predict:
        # every later detect_intent then fails with a confusing FAILED_PRECONDITION instead.
        if training_operation_update.HasField("error"):
            raise RuntimeError(
                "Training the agent failed. The agent is NOT trained and cannot detect intents. "
                f"code={training_operation_update.error.code} "
                f"message={training_operation_update.error.message!r}"
            )
        print(f"Agent {parent} trained successfully.")
