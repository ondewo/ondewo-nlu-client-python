import json

from ondewo.nlu.agent_pb2 import FullTextSearchRequest, FullTextSearchResponseIntent, \
    FullTextSearchResponseIntentContextIn, FullTextSearchResponseIntentContextOut, FullTextSearchResponseIntentUsersays, \
    FullTextSearchResponseIntentTags, FullTextSearchResponseIntentResponse, FullTextSearchResponseIntentParameters, \
    FullTextSearchResponseEntityType, FullTextSearchResponseEntity, FullTextSearchResponseEntitySynonym
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig


project_id: str = '<Your project ID>'
parent: str = f'projects/{project_id}/agent'
language_code: str = 'de'
config_file: str = 'examples/local_client.json'

with open(config_file) as f:
    config_ = json.load(f)

config = ClientConfig(
    host=config_["host"],
    port=config_["port"],
    user_name=config_["user_name"],
    password=config_["password"],
    http_token=config_["http_token"],
    grpc_cert=config_.get("grpc_cert", ''),
)

client: Client = Client(config=config, use_secure_channel=False)
print('Client created!')


def get_request(term: str) -> FullTextSearchRequest:
    request = FullTextSearchRequest(
        parent=parent,
        language_code=language_code,
        term=term,
    )
    return request


def test_search_intent(term: str) -> FullTextSearchResponseIntent:
    return client.services.agents.get_full_text_search_intent(
        request=get_request(term=term)
    )


def test_search_intent_context_in(term: str) -> FullTextSearchResponseIntentContextIn:
    return client.services.agents.get_full_text_search_intent_context_in(
        request=get_request(term=term)
    )


def test_search_intent_context_out(term: str) -> FullTextSearchResponseIntentContextOut:
    return client.services.agents.get_full_text_search_intent_context_out(
        request=get_request(term=term)
    )


def test_search_intent_usersays(term: str) -> FullTextSearchResponseIntentUsersays:
    return client.services.agents.get_full_text_search_intent_usersays(
        request=get_request(term=term)
    )


def test_search_intent_tags(term: str) -> FullTextSearchResponseIntentTags:
    return client.services.agents.get_full_text_search_intent_tags(
        request=get_request(term=term)
    )


def test_search_intent_response(term: str) -> FullTextSearchResponseIntentResponse:
    return client.services.agents.get_full_text_search_intent_response(
        request=get_request(term=term)
    )


def test_search_intent_parameters(term: str) -> FullTextSearchResponseIntentParameters:
    return client.services.agents.get_full_text_search_intent_parameters(
        request=get_request(term=term)
    )


def test_search_entity_type(term: str) -> FullTextSearchResponseEntityType:
    return client.services.agents.get_full_text_search_entity_type(
        request=get_request(term=term)
    )


def test_search_entity(term: str) -> FullTextSearchResponseEntity:
    return client.services.agents.get_full_text_search_entity(
        request=get_request(term=term)
    )


def test_search_entity_synonym(term: str) -> FullTextSearchResponseEntitySynonym:
    return client.services.agents.get_full_text_search_entity_synonym(
        request=get_request(term=term)
    )


def main():
    test_search_intent("*are*")
    test_search_intent_context_in("one")
    test_search_intent_context_in("two")
    test_search_intent_usersays("intent_one")
    test_search_intent_tags("intent_one")
    test_search_intent_parameters("parameter")
    test_search_intent_response("platform_unspecified")
    test_search_entity_type("one")
    test_search_entity("one")
    test_search_entity_synonym("two")


if __name__ == '__main__':
    main()
