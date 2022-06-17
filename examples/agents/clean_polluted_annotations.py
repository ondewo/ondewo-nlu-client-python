import json
from collections import defaultdict
from typing import Dict, Set, List

import tqdm as tqdm

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.entity_type_pb2 import ListEntityTypesRequest, EntityTypeView, ListEntityTypesResponse
from ondewo.nlu.intent_pb2 import ListTrainingPhrasesRequest, ListIntentsRequest, IntentView, \
    ListIntentsResponse, ListTrainingPhrasesResponse, Intent, BatchUpdateTrainingPhrasesRequest


def get_all_entities(parent: str, language_code: str, client: Client) -> Dict[str, Dict[str, Set[str]]]:
    _map: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))
    print('Creating Entity Map...')

    response: ListEntityTypesResponse = client.services.entity_types.list_entity_types(
        ListEntityTypesRequest(
            parent=parent,
            language_code=language_code,
            entity_type_view=EntityTypeView.ENTITY_TYPE_VIEW_FULL,
            page_token='page_size-100000'
        )
    )

    for et in tqdm.tqdm(iterable=response.entity_types, desc='Loading entity map...'):
        for ev in et.entities:
            _map[et.name][ev.name] = _map[et.name][ev.name].union({s for s in ev.synonyms})

    print('Entity Map created!')
    return _map


def check_all_annotations(parent: str, language_code: str, entity_map: Dict, client: Client,
                          dry_run: bool = False) -> None:
    intents_response: ListIntentsResponse = client.services.intents.list_intents(
        ListIntentsRequest(
            parent=parent,
            language_code=language_code,
            intent_view=IntentView.INTENT_VIEW_SHALLOW,
            page_token='page_size-10000000'
        )
    )

    phrases_to_update: List[Intent.TrainingPhrase] = []

    for intent in tqdm.tqdm(iterable=intents_response.intents, desc='Cleaning Training Phrases...'):

        phrases: ListTrainingPhrasesResponse = client.services.intents.list_training_phrases(
            ListTrainingPhrasesRequest(
                intent_name=intent.name,
                # intent_name='<Intent ID>',
                language_code=language_code,
                page_token='page_size-10000000'
            )
        )
        for phrase in phrases.training_phrases:
            annotations: List[Intent.TrainingPhrase.Entity] = []

            for annotation in phrase.entities:
                t: str = phrase.text[annotation.start:annotation.end]

                if (
                        not annotation.entity_type_display_name.startswith('sys.')
                        and t not in entity_map[annotation.entity_type_name][annotation.entity_value_name]
                ):
                    print(f'Annotation! "{t}" '
                          f'on intent [{intent.display_name}] '
                          f'has no synonym on the entity type: [{annotation.entity_type_display_name}]')

                    if dry_run:
                        annotations.append(annotation)
                else:
                    annotations.append(annotation)

            del phrase.entities[:]
            phrase.entities.extend(annotations)

        phrases_to_update.extend(phrases.training_phrases)

    if not dry_run:
        client.services.intents.batch_update_training_phrases(
            BatchUpdateTrainingPhrasesRequest(
                training_phrases=phrases_to_update
            )
        )


if __name__ == '__main__':
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

    map_: Dict[str, Dict[str, Set[str]]] = get_all_entities(
        parent=parent, language_code=language_code, client=client
    )
    check_all_annotations(
        parent=parent, language_code=language_code, entity_map=map_, client=client, dry_run=False
    )
