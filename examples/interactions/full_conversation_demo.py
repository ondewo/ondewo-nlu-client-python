import uuid
from typing import Optional, Dict

from ondewo.nlu import context_pb2
from ondewo.nlu.client import Client as NluClient
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.session_pb2 import DetectIntentResponse, DetectIntentRequest, QueryInput, TextInput, QueryParameters


def make_nlu_conversation(session):
    context_flag_input = str(input('Do you want to activate context? (y/n)'))
    context_flag = True if context_flag_input == 'y' else False
    conversation_nlu_helper(session, context_flag=context_flag)
    while True:
        text = input('you: ')
        if text == 'end convo':
            break
        conversation_nlu_helper(session, text)


def conversation_nlu_helper(session, text="Default Welcome Intent", context_flag=False):
    context = make_context() if context_flag else None
    nlu_response: DetectIntentResponse = get_response_from_request(session=session,
                                                                   text=text,
                                                                   context=context)
    print(f'Text received by the server: {nlu_response.query_result.query_text}')
    print(f'Intent detected: {nlu_response.query_result.intent.display_name}')

    for message in nlu_response.query_result.fulfillment_messages:
        print('bot: ', end='')
        print(message.text.text[0])


def get_response_from_request(session, text, context=None) -> DetectIntentResponse:
    context: Optional[context_pb2.Context] = [context] if context else None
    nlu_request: DetectIntentRequest = DetectIntentRequest(
        session=session,
        query_input=QueryInput(
            text=TextInput(
                text=text,
                language_code='de',
            )
        ),
        query_params=QueryParameters(
            contexts=context
        )
    )
    nlu_response: DetectIntentResponse = nlu_client.services.sessions.detect_intent(
        request=nlu_request,
    )
    return nlu_response


def make_context() -> context_pb2.Context:
    # Enter intent name .. Example would be i.order.pizza
    intent_name: str = "<intent_name>"
    context_parameter: context_pb2.Context.Parameter = context_pb2.Context.Parameter(
        display_name='intent_name',
        value=intent_name
    )

    # intent_name in display_name and parameter "dictionary" are hardcoded. So don't change them
    parameter: Dict[str, context_pb2.Context.Parameter] = {'intent_name': context_parameter}

    # Don't change the name, just change the lifespan_count, which defines how many times this context is going to be injected
    context = context_pb2.Context(
        name=f"{session}/contexts/exact_intent",
        lifespan_count=20,
        parameters=parameter
    )

    return context


def create_session_nlu(project_id: str) -> str:
    session_id: str = str(uuid.uuid4())
    project_parent: str = f'projects/{project_id}/agent'
    return f'{project_parent}/sessions/{session_id}'


if __name__ == '__main__':
    # Pass in your project id and a session will be created for the nlu client
    project_id: str = '<project id>'
    session: str = create_session_nlu(project_id)
    
    # Client configuration
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    nlu_client: NluClient = NluClient(config=config, use_secure_channel=False)

    # You have to go to the function and set the context you want
    context: context_pb2.Context = make_context()

    # Enter "end conversation" to quit at any time
    # Say y if you want to use context
    make_nlu_conversation(session)
