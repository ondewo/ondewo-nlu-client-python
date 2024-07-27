# Copyright 2021-2024 ONDEWO GmbH
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
from ondewo.nlu.session_pb2 import TextInput
from ondewo.qa.client import (
    Client as QAClient,
    ClientConfig,
)
from ondewo.qa.qa_pb2 import (
    GetAnswerRequest,
    GetAnswerResponse,
)

if __name__ == '__main__':
    config: ClientConfig = ClientConfig(
        host='localhost',
        port='1234'
    )
    client: QAClient = QAClient(
        config=config,
        use_secure_channel=False
    )

    answer: GetAnswerResponse = client.services.qa.get_answer(
        GetAnswerRequest(
            text=TextInput(text='<Your Q&A query>'),
            max_num_answers=3,
            threshold_reader=0,
            threshold_retriever=0
        )
    )

    print(answer.query_result)
