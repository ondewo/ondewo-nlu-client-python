import argparse
import os
import zipfile
from typing import List, Tuple

import polling
from google.longrunning.operations_pb2 import Operation, GetOperationRequest
from ondewo.logging.logger import logger_console as logger

from ondewo.nlu.agent_pb2 import ExportAgentRequest, ExportAgentResponse
from ondewo.nlu.agent_pb2 import ListAgentsRequest, AgentView, ListAgentsResponse
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
import json

def export_agents(args: argparse.Namespace) -> None:
    # Set the client configs and create a client instance
    config: ClientConfig = ClientConfig.from_json(args.config)
    client: Client = Client(config=config, use_secure_channel=args.secure)

    # example would be [("projects/2fa32d44-a654-4772-bebb-87fef894d0e5/agent,"ATC-startup project"),  ... ]
    agents_info: List[Tuple[str, str]] = get_agents_info(client=client)

    dir_path = create_path_if_not_exists(args)

    logger.info("Start exporting all agents \n ========================")

    # For each agent export it
    for agent_info in agents_info:
        parent: str = agent_info[0]
        project_id = parent.split('/')[1]
        display_name: str = agent_info[1]

        logger.info(f"Start exporting {display_name} project")
        export_operation: Operation = client.services.agents.export_agent(
            ExportAgentRequest(
                parent=parent
            )
        )

        polling.poll(
            target=client.services.operations.get_operation,
            step=1,
            args=(GetOperationRequest(name=export_operation.name),),
            check_success=lambda op: op.done,
            timeout=600,  # wait 10 minutes until training is finished
        )

        export_operation_update: Operation = client.services.operations.get_operation(
            GetOperationRequest(name=export_operation.name)
        )
        export_response: ExportAgentResponse = ExportAgentResponse()
        export_operation_update.response.Unpack(export_response)
        if export_response.agent_content:
            with open(f'{dir_path}/{display_name}.zip', mode='wb') as zf:
                zf.write(export_response.agent_content)
            zip_extract(dir_path)
            create_change_log_md(dir_path)
            create_project_name_md(dir_path, display_name, project_id)
            logger.info(f"End exporting {display_name} project")
        else:
            logger.warning(f"Failed to export {display_name} project")

    logger.info("======================== \n End exporting all agents")

def create_path_if_not_exists(args):
    exported_agents_dir_name: str = args.exported_agents_dir_name
    dir_path: str = os.path.join(os.getcwd(), exported_agents_dir_name)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return dir_path

def get_agents_info(client: Client) -> List[Tuple[str, str]]:
    # This will contain List containing tuples "which are the info of the agent" of each agent
    # so example would be [("projects/2fa32d44-a654-4772-bebb-87fef894d0e5/agent,"ATC-startup project"), ...]
    agents_info: List[Tuple[str, str]] = []
    # Set the page_size a high number to get all the agents
    page_size: int = 100_000
    agents: ListAgentsResponse = client.services.agents.list_all_agents(
        request=ListAgentsRequest(agent_view=AgentView.AGENT_VIEW_SHALLOW, page_token=f'page_size-{page_size}')
    )

    if agents.agents_with_owners:
        agents_info += [(agent.agent.parent, agent.agent.display_name) for agent in agents.agents_with_owners]

    # returns the parent and display name of all agents
    return agents_info

def zip_extract(directory: str) -> None:
    extension: str = ".zip"
    os.chdir(directory)
    for item in os.listdir(directory):  # loop through items in dir
        if item.endswith(extension):  # check for ".zip" extension
            zip_name: str = os.path.abspath(item)  # get full path of files
            file_name: str = (os.path.basename(zip_name)).rsplit('.', 1)[0]  # get file name for file within
            with zipfile.ZipFile(zip_name, 'r') as zipObj:
                # Extract all the contents of zip file in different directory
                zipObj.extractall(file_name)
            os.remove(zip_name)  # delete zipped file



def create_change_log_md(dir_path):
    projects_directories = get_all_directories(dir_path)
    for dir in projects_directories:
        base_path = os.path.abspath(dir)
        config_data = get_data_json(base_path)
        change_log_md = os.path.join(base_path,"CHANGELOG.MD")
        with open(change_log_md, 'w') as f:
            description = config_data["agent_config"]["description"]
            for d in description:
                f.write(d)

def create_project_name_md(dir_path,display_name,project_id):
    projects_directories = get_all_directories(dir_path)
    for dir in projects_directories:
        base_path = os.path.abspath(dir)
        project_name_md = os.path.join(base_path, "PROJECTNAME.MD")
        with open(project_name_md, 'w+') as f:
            f.write(display_name+'\n')
            f.write(project_id)

def get_all_directories(dir_path):
    projects_directories_iter: Tuple[str, List[str], List[str]] = next(os.walk(dir_path), ('', [], []))
    projects_directories: List[str] = projects_directories_iter[1]
    return projects_directories

def get_data_json(dir_path):
    config_path = os.path.join(dir_path, "OndewoConfig.json")
    with open(config_path) as f:
        config_data = json.load(f)
    return config_data

def arg_parse() -> argparse.Namespace:
    description: str = "Export example, so usage would be like: \n\n" \
                       "\t\tpython -m export --config=\"$(cat conf.json)\" --exported-agents-dir-name=2.6.x --secure"
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--config", type=str, required=True)
    parser.add_argument("--exported-agents-dir-name", type=str, required=True)
    parser.add_argument("--secure", default=False, action="store_true", required=False)
    args: argparse.Namespace = parser.parse_args()
    return args

if __name__ == '__main__':
    args = arg_parse()
    export_agents(args=args)