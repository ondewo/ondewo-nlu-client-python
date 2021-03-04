from typing import Optional

import polling
from google.longrunning.operations_pb2 import Operation, GetOperationRequest

from ondewo.nlu.agent_pb2 import RestoreAgentRequest
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig

if __name__ == '__main__':
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    zip_path: str = '<the path of your zip file>'
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>',
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
