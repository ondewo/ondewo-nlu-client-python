import json

import polling
from google.longrunning.operations_pb2 import Operation, GetOperationRequest

from ondewo.nlu.agent_pb2 import ExportAgentRequest, ExportAgentResponse
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig

if __name__ == '__main__':
    parent: str = 'projects/some_agent_id/agent'
    config_file: str = 'envs/example.json'

    with open(config_file) as f:
        config_ = json.load(f)

    config = ClientConfig(
        host=config_["host"],
        port=config_["port"],
        user_name=config_["user_name"],
        password=config_["password"],
        http_token=config_["http_token"],
        grpc_cert=config_.get("grpc_cert", '').encode().decode().replace("\\n", "\n"),  # type: ignore
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

    export_operation_update: Operation = client.services.operations.get_operation(
        GetOperationRequest(name=export_operation.name)
    )
    export_response: ExportAgentResponse = ExportAgentResponse()
    export_operation_update.response.Unpack(export_response)
    assert export_response.agent_content

    with open('my_backup.zip', mode='wb') as zf:
        zf.write(export_response.agent_content)
