'''

'''


from ondewo.nlu.client import Client as NluClient
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.session_pb2 import DetectIntentResponse, DetectIntentRequest, \
    QueryInput, TextInput, QueryParameters, DeleteSessionRequest

if __name__ == '__main__':
    # Pass in your project id and a session will be created for the nlu client
    project_id: str = '<project id>'
    project_parent: str = f'projects/{project_id}/agent'
    session_id = '<session_id>'
    session_path: str = f'{project_parent}/sessions/{session_id}'

    # Client configuration
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    nlu_client: NluClient = NluClient(config=config, use_secure_channel=False)

    # DELETE a session
    nlu_client.services.sessions.delete_session(DeleteSessionRequest(session_id=session_path))

    # Nlu request and response
    nlu_request: DetectIntentRequest = DetectIntentRequest(
        session=session_path,
        query_input=QueryInput(
            text=TextInput(
                text="<enter your text here>",
                language_code='de',
            )
        ),
        query_params=QueryParameters(
        )
    )
    nlu_response: DetectIntentResponse = nlu_client.services.sessions.detect_intent(
        request=nlu_request,
    )

    print(f'Text received by the server: {nlu_response.query_result.query_text}')
    print(f'Intent detected: {nlu_response.query_result.intent.display_name}')
    print('Text response:')
    for message in nlu_response.query_result.fulfillment_messages:
        print(message.text.text[0])
