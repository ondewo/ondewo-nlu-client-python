# Copyright 2021 ONDEWO GmbH
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


from dataclasses import dataclass
from typing import Optional, TypeVar, Dict, Type, Any
from uuid import uuid4

from google.protobuf.message import Message

from ondewo.nlu.context_pb2 import CreateContextRequest, ListContextsRequest, UpdateContextRequest, \
    DeleteContextRequest, DeleteAllContextsRequest, GetContextRequest
from ondewo.nlu.intent_pb2 import GetIntentRequest, ListIntentsRequest, CreateIntentRequest, \
    UpdateIntentRequest, DeleteIntentRequest, BatchUpdateIntentsRequest, BatchDeleteIntentsRequest
from ondewo.nlu.session_pb2 import DetectIntentRequest, GetLatestSessionReviewRequest, ListSessionsRequest, \
    GetSessionRequest, ListSessionReviewsRequest, GetSessionReviewRequest, CreateSessionReviewRequest
from ondewo.nlu.user_pb2 import LoginRequest
from ondewo.utils.helpers import get_attr_recursive, set_attr_recursive

T = TypeVar("T", bound=Message)


@dataclass
class SharedRequestData(object):
    """
    Dataclass for sharing data among different requests.

    Example:

    Attributes:
        project_parent: Optional[str] = None ... the identifier for the NLU project (format 'projects/<ID>/agent')
        language_code: Optional[str] = None ... the language code (e.g., 'en', 'de', etc)
        intent_uuid: Optional[str] = None ... the UUID identifying an intent
        session_uuid: Optional[str] = None ... the UUID identifying an NLU session
        session_review_uuid: Optional[str] = None ... the UUID identifying an NLU session review

    """
    project_parent: Optional[str] = None
    language_code: Optional[str] = None
    intent_uuid: Optional[str] = None
    session_uuid: Optional[str] = None
    session_review_uuid: Optional[str] = None

    def set_fresh_session_uuid(self, uuid: Optional[str] = None) -> str:
        uuid_: str = uuid or str(uuid4())
        self.session_uuid = uuid_
        return self.session_uuid

    @property
    def session_id(self) -> Optional[str]:
        if not self.project_parent or not self.session_uuid:
            return None
        return f'{self.project_parent}/sessions/{self.session_uuid}'

    @property
    def session_review_id(self) -> Optional[str]:
        if not self.project_parent or not self.session_uuid:
            return None
        return f'{self.project_parent}/sessions/{self.session_uuid}/reviews/{self.session_review_uuid}'

    @property
    def intent_id(self) -> Optional[str]:
        if not self.project_parent or not self.intent_uuid:
            return None
        return f'{self.project_parent}/intents/{self.intent_uuid}'

    def fill_missing_fields(self, request: T) -> T:
        """
        Fill fields of the request which are not set with corresponding values from self.
        Note: Does not modify the request in place but returns a copy with updated fields.

        Args:
            request (Message):

        Returns:
            Message: The request with the additional fields.

        Raises:
            ValueError: if, for a field which is not set on the request,
             ... and which should be gotten from self, no value is set on self.

            NotImplementedError: if the mapping from request fields to fields of self is not set for the request type.
        """
        # The mapping from request fields to corresponding fields of self is specified for each request type
        #         ... in the dictionary _request_field__to__field__per__request_type
        request_type: Type[T] = type(request)
        request_to_return: T = request_type()
        request_to_return.MergeFrom(request)

        if request_type not in self._request_field__to__field__per__request_type:
            raise NotImplementedError(f'mapping not defined for request type "{request_type}".')

        request_field__to__field: Dict[str, str] = \
            self._request_field__to__field__per__request_type[request_type]
        for request_field_name, field_name in request_field__to__field.items():
            value_from_request: Any = get_attr_recursive(obj=request_to_return, attr=request_field_name)
            if not value_from_request:
                value_from_self: Any = get_attr_recursive(obj=self, attr=field_name)
                if not value_from_self:
                    raise ValueError(f'Could not get {field_name} for {self}.')

                set_attr_recursive(obj=request_to_return, attr=request_field_name, value=value_from_self)
        return request_to_return

    @property
    def _request_field__to__field__per__request_type(
            self,
    ) -> Dict[Any, Dict[str, str]]:  # fixme: return type should be  Dict[Type[T], Dict[str, str]]
        """
        _request_field__to__field__per__request_type specifies ...
        ... how to fill fields which are not set on a request with fields of self
        ... (for every request-type accepted by the methods exposed under client.services.<service_name>)

        Example:
           DetectIntentRequest: {
                'session': 'session',
                'query_input.text.language_code': 'language_code'
            }
        ... means that for any DetectIntentRequest processed by the client:
              - request.session should be set to self.session if unset
              - request.query_input.text.language_code should be set to self.language_code if unset

        """
        return {
            DetectIntentRequest: {
                'session': 'session_id',
                'query_input.text.language_code': 'language_code'
            },
            ListSessionsRequest: {
                'parent': 'project_parent',
            },
            GetSessionRequest: {
                'session_id': 'session_id'
            },
            ListSessionReviewsRequest: {
                'session_id': 'session_id'
            },
            GetSessionReviewRequest: {
                'session_review_id': 'session_review_id'
            },
            GetLatestSessionReviewRequest: {
                'session_id': 'session_id'
            },
            CreateSessionReviewRequest: {
                'session_id': 'session_id'
            },
            CreateContextRequest: {
                'parent': 'session_id',
            },
            ListContextsRequest: {
                'parent': 'session_id',
            },
            GetContextRequest: {
            },
            UpdateContextRequest: {
            },
            DeleteContextRequest: {
            },
            DeleteAllContextsRequest: {
                'parent': 'project_parent',
            },
            LoginRequest: {},
            GetIntentRequest: {
                'name': 'intent_id',
                'language_code': 'language_code',
            },
            ListIntentsRequest: {
                'parent': 'project_parent',
                'language_code': 'language_code',
            },
            CreateIntentRequest: {
                'parent': 'project_parent',
                'language_code': 'language_code',
                'intent.name': 'intent_id',
            },
            UpdateIntentRequest: {
                'language_code': 'language_code',
                'intent.name': 'intent_id',
            },
            DeleteIntentRequest: {
                'name': 'intent_id',
            },
            BatchUpdateIntentsRequest: {
                'parent': 'project_parent',
                'language_code': 'language_code',
            },
            BatchDeleteIntentsRequest: {
                'parent': 'project_parent',
            },
        }
