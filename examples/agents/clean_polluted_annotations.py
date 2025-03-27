# Copyright 2021-2025 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import asyncio
import json
import os.path
from collections import defaultdict
from typing import (
    Dict,
    List,
    Set,
)

import tqdm as tqdm
from ondewo.logging.decorators import Timer
from ondewo.logging.logger import logger_console as log

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.entity_type_pb2 import (
    EntityTypeView,
    ListEntityTypesRequest,
    ListEntityTypesResponse,
)
from ondewo.nlu.intent_pb2 import (
    BatchUpdateTrainingPhrasesRequest,
    Intent,
    IntentView,
    ListIntentsRequest,
    ListIntentsResponse,
    ListTrainingPhrasesRequest,
    ListTrainingPhrasesResponse,
)


@Timer(logger=log.debug, log_arguments=True, message='Retrieving all entities. Elapsed time: {}')
def get_all_entities(
    parent: str,
    language_code: str,
    client: Client
) -> Dict[str, Dict[str, Set[str]]]:
    log.debug('START: Creating Entity Map...')
    _map: Dict[str, Dict[str, Set[str]]] = defaultdict(lambda: defaultdict(set))

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
            _map[et.name][ev.name] |= {s for s in ev.synonyms}  # Merge sets together in place

    log.debug('DONE: Creating Entity Map.')
    return _map


@Timer(logger=log.debug, log_arguments=True, message='Checking all annotations. Elapsed time: {}')
async def check_all_annotations(
    parent: str,
    language_code: str,
    entity_map: Dict,
    client: Client,
    dry_run: bool = False
) -> None:
    log.debug("START: Retrieving the intent list...")
    intents_response: ListIntentsResponse = client.services.intents.list_intents(
        ListIntentsRequest(
            parent=parent,
            language_code=language_code,
            intent_view=IntentView.INTENT_VIEW_MINIMUM,
            page_token='page_size-10000000'
        )
    )
    nr_of_intents: int = len(intents_response.intents)
    log.debug(f'DONE: Retrieving the intent list of {nr_of_intents} intents')

    phrases_to_update: List[Intent.TrainingPhrase] = []
    for intent in tqdm.tqdm(iterable=intents_response.intents, desc='Cleaning Training Phrases...'):
        list_training_phrase_response: ListTrainingPhrasesResponse = client.services.intents.list_training_phrases(
            ListTrainingPhrasesRequest(
                intent_name=intent.name,  # intent_name='<Intent ID>',
                language_code=language_code,
                page_token='page_size-10000000'  # get all training phrases of the intent
            )
        )
        phrases_to_update_in_intent: List[Intent.TrainingPhrase] = []
        nr_of_training_phrass_in_intent: int = len(list_training_phrase_response.training_phrases)
        log.debug(f'START: Cleaning {nr_of_training_phrass_in_intent} training phrases in intent {intent.display_name}')

        for phrase in list_training_phrase_response.training_phrases:
            annotations: List[Intent.TrainingPhrase.Entity] = []

            annotations_before_cleaning: int = len(phrase.entities)
            if annotations_before_cleaning == 0:
                continue

            for annotation in phrase.entities:
                t: str = phrase.text[annotation.start:annotation.end]

                if (
                    not annotation.entity_type_display_name.startswith('sys.') and
                    t not in entity_map[annotation.entity_type_name][annotation.entity_value_name]
                ):
                    log.debug(
                        f'Annotation! "{t}" '
                        f'on intent [{intent.display_name}] '
                        f'has no synonym on the entity type: [{annotation.entity_type_display_name}]'
                    )

                    if dry_run:
                        # Only, if dry run, then keep entity annotation if synonym is in our domain else don't
                        annotations.append(annotation)
                else:
                    # keep entity annotation if synonym is in our domain
                    annotations.append(annotation)

            # only include training phrases in the update if the annotations have been reduced
            annotations_after_cleaning: int = len(annotations)
            if annotations_before_cleaning > annotations_after_cleaning:
                del phrase.entities[:]
                phrase.entities.extend(annotations)
                phrases_to_update_in_intent.extend([phrase])

        nr_of_cleaned_training_phrases_of_intent: int = len(phrases_to_update_in_intent)
        if nr_of_cleaned_training_phrases_of_intent > 0:
            log.debug(
                f'DONE: Cleaned {nr_of_cleaned_training_phrases_of_intent} of {nr_of_training_phrass_in_intent} '
                f'training phrases in intent {intent.display_name}.'
            )
            phrases_to_update.extend(phrases_to_update_in_intent)
        else:
            log.debug(
                f'DONE: No cleaning was necessary for {nr_of_training_phrass_in_intent} '
                f'training phrases in intent {intent.display_name}.'
            )

    if not dry_run:
        nr_of_training_phrases_to_update = len(phrases_to_update)
        if nr_of_training_phrases_to_update > 0:
            log.info(
                f'START: Updating {nr_of_training_phrases_to_update} training phrases in '
                f'{nr_of_intents} intents...'
            )

            chunk_size: int = 100
            training_phrase_chunks: List[List[Intent.TrainingPhrase]] = [
                phrases_to_update[x:x + chunk_size] for x in range(0, nr_of_training_phrases_to_update, chunk_size)
            ]
            log.debug(f'Split training phrases into {training_phrase_chunks} chunks of chunk size {chunk_size}')
            tasks = [batch_update_training_phrase(client, chunk) for chunk in training_phrase_chunks]
            await asyncio.wait(tasks)

            log.info(
                f'DONE: Updating {nr_of_training_phrases_to_update} training phrases in '
                f'{nr_of_intents} intents.'
            )
        else:
            log.info(f'No training phrases need to be cleaned. Checked {nr_of_intents} intents.')


@Timer(logger=log.debug, log_arguments=False, message='batch_update_training_phrase. Elapsed time: {}')
async def batch_update_training_phrase(
    client: Client,
    phrases_to_update: List[Intent.TrainingPhrase]
) -> None:
    client.services.intents.batch_update_training_phrases(
        BatchUpdateTrainingPhrasesRequest(
            training_phrases=phrases_to_update
        )
    )


if __name__ == '__main__':
    log.info(
        """
            ------------------------------------------------------------------------
              INFO: This script removes all annotations that mark text that is not
              part of the synonyms of the associated entity value and entity type
            ------------------------------------------------------------------------
            """
    )
    ################################################################################
    # Update here your configuration for the project and the nlu client            #
    ################################################################################
    project_id: str = '652c101f-fe0a-4956-8fd2-1a80b21c4348'  # project_id: str = '<Your project ID>'
    language_code: str = 'de'
    config_file: str = 'examples/local_client.json'  # config file for the ClientConfig

    # region Client configuration
    # default client settings
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234',
        http_token='aimp',
        user_name='admin@ondewo.com',
        password='asdf'
    )

    # in configuration file exists overwrite the standard client configuration
    if os.path.isfile(config_file):
        with open(config_file) as f:
            config_ = json.load(f)
        config = ClientConfig(
            host=config_['host'],
            port=config_['port'],
            user_name=config_['user_name'],
            password=config_['password'],
            http_token=config_['http_token'],
            grpc_cert=config_.get('grpc_cert', ''),
        )
    # endregion

    log.info('Starting clean up process ... ')
    parent: str = f'projects/{project_id}/agent'
    client: Client = Client(config=config, use_secure_channel=False)
    log.debug('Client created!')
    map_: Dict[str, Dict[str, Set[str]]] = get_all_entities(
        parent=parent,
        language_code=language_code,
        client=client,
    )

    # Create an asyncio loop to run batch update in parallel
    asyncio.run(
        check_all_annotations(
            parent=parent,
            language_code=language_code,
            entity_map=map_,
            client=client,
            dry_run=False,
        )
    )
    log.info('Clean up process complete!!')
