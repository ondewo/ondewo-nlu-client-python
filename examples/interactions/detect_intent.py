from faker import Faker

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.session_pb2 import DetectIntentResponse, DetectIntentRequest, QueryInput, TextInput

if __name__ == '__main__':
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    client: Client = Client(config=config, use_secure_channel=False)
    f: Faker = Faker()
    session_name: str = f.name()

    request: DetectIntentRequest = DetectIntentRequest(
        session=f'{parent}/sessions/{session_name}',
        query_input=QueryInput(
            text=TextInput(text='<Some text>')
        )
    )

    response: DetectIntentResponse = client.services.sessions.detect_intent(request=request)

    print(f'Text received by the server: {response.query_result.query_text}')
    print(f'Intent detected: {response.query_result.intent.display_name}')
    print(f'Text response: {response.query_result.fulfillment_messages[0].text.text[0]}')
