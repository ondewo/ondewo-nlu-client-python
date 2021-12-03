from ondewo.nlu import intent_pb2
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig

if __name__ == '__main__':
    # CONFIGURING THE CLIENT
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )
    client: Client = Client(config=config, use_secure_channel=False)

    # CONFIGURING THE AGENT
    parent: str = '<PUT_YOUR_AGENT_PARENT_HERE>'
    language_code: str = '<acronym of he language of choice, i.e "en">'

    r = intent_pb2.CreateIntentRequest(
        intent=intent_pb2.Intent(
            display_name='i.pepper.dance',
            webhook_state=intent_pb2.Intent.WEBHOOK_STATE_UNSPECIFIED,
            priority=250000,
            is_fallback=False,
            input_context_names=[],
            messages=[
                intent_pb2.Intent.Message(
                    text=intent_pb2.Intent.Message.Text(
                        text=[
                            'Hast du nicht die Fotos vom letzten Wochenende gesehen? ',
                            'Pass mal auf.  $onStartBehavior=ht_entertainment/dance', ]
                    )
                ),
                intent_pb2.Intent.Message(
                    platform=intent_pb2.Intent.Message.Platform.FACEBOOK,
                    text=intent_pb2.Intent.Message.Text(
                        text=[
                            'FACEBOOK',
                            'FACEBOOK ffuscd', ]
                    )
                ),
                intent_pb2.Intent.Message(
                    platform=intent_pb2.Intent.Message.Platform.KIK,
                    text=intent_pb2.Intent.Message.Text(
                        text=[
                            'PLATFORM 12 rocks!', ]
                    )
                )

            ],
            training_phrases=[
                intent_pb2.Intent.TrainingPhrase(
                    text='@pepper:pepper kannst du tanzen?',
                    type=intent_pb2.Intent.TrainingPhrase.TEMPLATE,
                ),
                intent_pb2.Intent.TrainingPhrase(
                    text='@pepper:pepper kannst du essen?',
                    type=intent_pb2.Intent.TrainingPhrase.TEMPLATE
                )
            ]
        ),
        parent=parent,
        language_code='en'
    )

    response = client.services.intents.create_intent(r)
    print(response)
    print(
        client.services.intents.get_intent(
            intent_pb2.GetIntentRequest(
                name=response.name,
                language_code='en'
            )
        )
    )
