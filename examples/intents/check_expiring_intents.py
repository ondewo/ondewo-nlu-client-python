import datetime
from typing import List

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.intent_pb2 import Intent, ListIntentsRequest, IntentView, IntentCategory

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

    # LOAD ALL INTENTS
    intents: List[Intent] = list(
        client.services.intents.list_intents(
            ListIntentsRequest(
                parent=parent,
                language_code=language_code,
                intent_view=IntentView.INTENT_VIEW_SHALLOW,
                filter_by_category=IntentCategory.DATE_ACTIVE_INTENTS,
                page_token='page_size-10000',
            )
        ).intents
    )

    expire_soon: List[Intent] = []
    end_date_limit: datetime.datetime = datetime.datetime.now() + datetime.timedelta(weeks=1)

    for i in intents:
        if i.end_date.ToDatetime() < end_date_limit:
            expire_soon.append(i)

    expire_soon.sort(key=lambda intent: intent.end_date.ToDatetime(), reverse=False)
    for i in expire_soon:
        print(i.display_name)
