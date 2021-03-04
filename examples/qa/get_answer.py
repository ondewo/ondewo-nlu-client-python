from ondewo.nlu.session_pb2 import TextInput
from ondewo.qa.client import Client as QAClient
from ondewo.qa.client import ClientConfig
from ondewo.qa.qa_pb2 import GetAnswerRequest, GetAnswerResponse

if __name__ == '__main__':
    config: ClientConfig = ClientConfig(
        host='<host>',
        port='<port>'
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
