import io
import json
from zipfile import ZipFile

from ondewo.nlu import agent_pb2, intent_pb2, project_statistics_pb2, common_pb2
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig


def get_agent_stats(client: Client, parent: str, language_code: str):
    response: agent_pb2.GetAgentStatisticsResponse = client.services.agents.get_agent_statistics(
        agent_pb2.GetAgentStatisticsRequest(
            parent=parent,
            format=agent_pb2.ReportFormat.CSV,
            language_code=language_code,
            type=agent_pb2.ReportType.ALL,
        )
    )
    zipped_reports: ZipFile = ZipFile(io.BytesIO(response.reports))
    zipped_reports.extractall('results/')
    print('Done')


def get_responses_per_intent(client: Client, parent: str, language_code: str):
    response: intent_pb2.ListIntentsResponse = client.services.intents.list_intents(
        intent_pb2.ListIntentsRequest(
            parent=parent,
            language_code=language_code,
            intent_view=intent_pb2.INTENT_VIEW_SHALLOW,
            page_token='page_size-10000000'
        )
    )

    with open('results/n_responses.csv', 'w') as f:
        f.write('intent id,')
        f.write('intent name,')
        f.write('n. responses')
        f.write('\n')

        for i in response.intents:
            response_count: common_pb2.StatResponse = client.services.project_statistics.get_response_count(
                project_statistics_pb2.GetProjectElementStatRequest(
                    name=i.name,
                    language_code=language_code
                )
            )

            f.write(f'{i.name},')
            f.write(f'{i.display_name},')
            f.write(str(response_count.value))
            f.write('\n')


if __name__ == '__main__':
    project_id: str = '<Your project ID>'
    parent: str = f'projects/{project_id}/agent'
    language_code: str = 'de'
    config_file: str = 'local_client.json'

    with open(config_file) as f:
        config_ = json.load(f)

    config = ClientConfig(
        host=config_["host"],
        port=config_["port"],
        user_name=config_["user_name"],
        password=config_["password"],
        http_token=config_["http_token"],
        grpc_cert=config_.get("grpc_cert", ''),  # type: ignore
    )

    client: Client = Client(config=config, use_secure_channel=False)
    print('Client created!')

    get_agent_stats(client=client, parent=parent, language_code=language_code)
    get_responses_per_intent(client=client, parent=parent, language_code=language_code)
