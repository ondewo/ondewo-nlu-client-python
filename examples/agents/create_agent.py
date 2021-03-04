import polling

from ondewo.nlu.agent_pb2 import CreateAgentRequest, Agent, ListAgentsRequest, GetAgentRequest, \
    ExportAgentRequest, ExportAgentResponse
from google.longrunning.operations_pb2 import Operation, GetOperationRequest
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.intent_pb2 import CreateIntentRequest, Intent, ListIntentsRequest

if __name__ == '__main__':
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    client: Client = Client(config=config, use_secure_channel=False)

    created_agent: Agent = client.services.agents.create_agent(
        CreateAgentRequest(
            agent=Agent(
                display_name='my python agent',
                default_language_code='en',
                supported_language_codes=['en'],
                time_zone='Europe/Vienna',
                nlu_platform='ONDEWO',
                description='This is an agent created through the python client'
            )
        )
    )

    print(client.services.agents.list_agents(ListAgentsRequest()))
    print(client.services.agents.get_agent(GetAgentRequest(parent=created_agent.parent)))

    created_intent: Intent = client.services.intents.create_intent(
        CreateIntentRequest(
            parent=created_agent.parent,
            language_code='en',
            intent=Intent(
                display_name='i.my_python_intent',
                training_phrases=[
                    Intent.TrainingPhrase(
                        type=Intent.TrainingPhrase.Type.EXAMPLE,
                        parts=[
                            Intent.TrainingPhrase.Part(
                                user_defined=True,
                                text='This is a training phrase'
                            )
                        ]
                    )
                ]
            )
        )
    )

    print(
        client.services.intents.list_intents(
            ListIntentsRequest(parent=created_agent.parent, language_code='en')
        )
    )

    export_operation: Operation = client.services.agents.export_agent(
        ExportAgentRequest(
            parent=created_agent.parent
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
