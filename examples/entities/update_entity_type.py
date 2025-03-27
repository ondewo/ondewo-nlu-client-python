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
from typing import List

from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.entity_type_pb2 import (
    ENTITY_TYPE_VIEW_FULL,
    EntityType,
    GetEntityTypeRequest,
    UpdateEntityTypeRequest,
)

if __name__ == '__main__':
    # CONFIGURING THE CLIENT
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234',
        http_token='<http/root token>',
        user_name='<e-mail of user>',
        password='<password of user>'
    )

    client: Client = Client(config=config, use_secure_channel=False)

    # CONFIGURING THE AGENT
    project_uuid: str = "02534e0c-0c4e-4977-9aee-332cbb7fafea"
    parent: str = f'projects/{project_uuid}/agent'  # projects/<project_id>/agent
    language_code: str = 'de'  # acronym of the language of choice, i.e "en"
    entity_type_uuid: str = "ff77e8a2-f414-4f57-aca7-53229c1bf679"
    entity_type_name: str = f"{parent}/entityTypes/{entity_type_uuid}"

    # retrieve the entity type including all values and synonyms, hence we need to set ENTITY_TYPE_VIEW_FULL
    # https://ondewo.github.io/ondewo-nlu-api/#ondewo.nlu.EntityTypes.GetEntityType
    get_entity_type_request: GetEntityTypeRequest = GetEntityTypeRequest(
        name=entity_type_name,
        language_code=language_code,
        entity_type_view=ENTITY_TYPE_VIEW_FULL,
    )
    entity_type: EntityType = client.services.entity_types.get_entity_type(get_entity_type_request)
    # here is the full entity type
    print(entity_type)

    # here are only our entities
    print(entity_type.entities)

    # Update the entity type means to replace the entity values and synonyms with the ones in the request
    # so we need to add further entities and synonyms to the EntityType
    # https://ondewo.github.io/ondewo-nlu-api/#ondewo.nlu.EntityTypes.UpdateEntityType

    # Step 1: delete all entities from the entity type incl. the meta information about entities and synonyms
    entity_type.ClearField("entities")
    entity_type.ClearField("entity_count")
    entity_type.ClearField("synonym_count")

    # Step 2: create the list of new entity values with
    new_entities: List[EntityType.Entity] = [
        EntityType.Entity(
            value='my new entity value number',
            synonyms=['my new synonym 1', 'my new synonym 2']
        ),
        EntityType.Entity(
            value='my new entity value letter',
            synonyms=['my new synonym a', 'my new synonym b']
        )
    ]

    # Step 3: add the new entities to our entity type
    entity_type.entities.extend(new_entities)

    # Step 4: create and send the update entity type request
    update_entity_type_request: UpdateEntityTypeRequest = UpdateEntityTypeRequest(
        entity_type=entity_type,
        language_code=language_code,
    )
    entity_type = client.services.entity_types.update_entity_type(update_entity_type_request)

    # Let's get again the entity type to see that it has been updated on the server side
    get_entity_type_request = GetEntityTypeRequest(
        name=entity_type_name,
        language_code=language_code,
        entity_type_view=ENTITY_TYPE_VIEW_FULL,
    )
    entity_type_updated: EntityType = client.services.entity_types.get_entity_type(get_entity_type_request)

    # here is the full entity type after the update
    print(entity_type_updated)

    # here are only our entities after the update
    print(entity_type.entities)
