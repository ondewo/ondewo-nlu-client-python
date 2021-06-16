import polling
from google.longrunning.operations_pb2 import Operation, GetOperationRequest

from ondewo.nlu.agent_pb2 import TrainAgentRequest
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig

if __name__ == '__main__':
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>',
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

    training_operation_update: Operation = client.services.operations.get_operation(
        GetOperationRequest(name=train_operation.name)
    )
    assert training_operation_update.done
