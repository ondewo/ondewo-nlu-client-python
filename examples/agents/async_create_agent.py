import sys
from pathlib import Path
import asyncio
import time
from typing import Optional

from loguru import logger as log

from ondewo.nlu.agent_pb2 import (
    Agent,
    CreateAgentRequest,
    ExportAgentRequest,
    ExportAgentResponse,
    GetAgentRequest,
    ListAgentsRequest,
    ListAgentsResponse,
)
from ondewo.nlu.async_client import AsyncClient
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.intent_pb2 import (
    CreateIntentRequest,
    GetIntentRequest,
    Intent,
    ListIntentsRequest,
    ListIntentsResponse,
)
from ondewo.nlu.operations_pb2 import (
    GetOperationRequest,
    Operation,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from example_env import (  # noqa: E402
    env,
    get_client_config,
    use_secure_channel,
)


async def poll_async(
    client: AsyncClient,
    operation_name: str,
    timeout: int = 600,
    check_interval: int = 1,
) -> Operation:
    """Polls an asynchronous operation until it completes or times out.

    Args:
        client: The async client instance.
        operation_name: The name of the operation to poll.
        timeout: Maximum time (in seconds) to wait for completion.
        check_interval: Time (in seconds) between polling attempts.

    Returns:
        The completed operation.

    Raises:
        TimeoutError: If the operation does not complete within the timeout.
    """
    deadline: float = time.monotonic() + timeout

    while True:
        operation: Optional[Operation] = await client.services.operations.get_operation(
            GetOperationRequest(name=operation_name),
        )
        if operation is None:
            raise RuntimeError(f"Failed to retrieve operation {operation_name} (received None).")

        if operation.done:
            return operation

        if time.monotonic() >= deadline:
            raise TimeoutError(f"Operation {operation_name} exceeded timeout of {timeout} seconds.")

        await asyncio.sleep(check_interval)


async def main() -> None:
    config: ClientConfig = get_client_config()
    # Use the async version of the client
    client: AsyncClient = AsyncClient(config=config, use_secure_channel=use_secure_channel())

    # Creating the agent
    created_agent: Agent = await client.services.agents.create_agent(
        CreateAgentRequest(
            agent=Agent(
                display_name="my python agent",
                default_language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
                supported_language_codes=["en-US"],
                time_zone="Europe/Vienna",
                nlu_platform="ONDEWO",
                description="This is an agent created through the python client",
            )
        )
    )

    # Getting the created agent and listing agents
    agent: Agent = await client.services.agents.get_agent(GetAgentRequest(parent=created_agent.parent))
    agent_list: ListAgentsResponse = await client.services.agents.list_agents(ListAgentsRequest())
    log.debug(f"Agent created: {agent}")
    log.debug(f"List of agents: {agent_list}")

    # Creating the intent
    created_intent: Intent = await client.services.intents.create_intent(
        CreateIntentRequest(
            parent=created_agent.parent,
            language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"),
            intent=Intent(
                display_name="i.pepper.dance",
                webhook_state=Intent.WEBHOOK_STATE_UNSPECIFIED,
                priority=250000,
                is_fallback=False,
                input_context_names=[],
                messages=[
                    Intent.Message(
                        text=Intent.Message.Text(
                            text=[
                                "Hast du nicht die Fotos vom letzten Wochenende gesehen? Pass mal auf.  "
                                "$onStartBehavior=ht_entertainment/dance",
                            ]
                        )
                    )
                ],
                training_phrases=[
                    Intent.TrainingPhrase(text="Pepper kannst du tanzen?", type=Intent.TrainingPhrase.EXAMPLE)
                ],
                status=Intent.IntentStatus.ACTIVE,
            ),
        )
    )

    intent: Intent = await client.services.intents.get_intent(GetIntentRequest(name=created_intent.name))
    intent_list: ListIntentsResponse = await client.services.intents.list_intents(
        ListIntentsRequest(parent=created_agent.parent, language_code=env("ONDEWO_NLU_CAI_LANGUAGE_CODE"))
    )
    log.debug(f"Intent created: {intent}")
    log.debug(f"List of intents: {intent_list}")

    # Exporting the agent
    export_operation: Operation = await client.services.agents.export_agent(
        ExportAgentRequest(parent=created_agent.parent)
    )
    log.debug(f"START: {export_operation.name}. Exporting agent {created_agent.parent}.")
    start_time: float = time.perf_counter()

    # Polling for the operation result asynchronously
    try:
        export_operation = await poll_async(client, export_operation.name)
    except TimeoutError as e:
        log.error(str(e))
        return

    log.debug(
        f"DONE: {export_operation.name}. Exported agent {created_agent.parent} "
        f"in {time.perf_counter() - start_time:.5f} sec."
    )

    # Retrieve the final operation status
    export_operation_update: Optional[Operation] = await client.services.operations.get_operation(
        GetOperationRequest(name=export_operation.name)
    )
    assert export_operation_update
    export_response: ExportAgentResponse = ExportAgentResponse()
    export_operation_update.response.Unpack(export_response)
    assert export_response.agent_content

    with open(env("ONDEWO_NLU_CAI_AGENT_ZIP_PATH"), mode="wb") as zf:
        zf.write(export_response.agent_content)


# Run the main async function
if __name__ == "__main__":
    asyncio.run(main())
