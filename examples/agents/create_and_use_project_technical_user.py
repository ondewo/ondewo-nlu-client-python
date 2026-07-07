"""
Create and use a project-scoped **technical user** with the ONDEWO NLU Python client.

A *project technical user* is a normal but **2FA-exempt** Keycloak account that holds the
``PROJECT_EXECUTOR`` (runtime) role on exactly **one** project. It exists so that headless
machine clients (e.g. ondewo-sip / csi / vtsi, CI jobs, your own backend) can authenticate to
the ONDEWO CAI backend without an interactive TOTP step, using the Keycloak Resource-Owner
Password-Credentials (ROPC) *offline-token* flow.

The end-to-end flow this script demonstrates:

  1. An **admin / project-developer** (someone holding ``AGENTS_CREATE_PROJECT_TECHNICAL_USER``
     — i.e. ``PROJECT_DEVELOPER`` or ``PROJECT_ADMIN`` on the target project) authenticates to
     CAI via Keycloak.
  2. They call ``create_project_technical_user`` on the **Agents** service. The server mints a
     Keycloak user, grants it ``PROJECT_EXECUTOR`` on the project, and returns its
     ``user_id`` / ``username`` and a generated ``password``. **The password is shown ONCE and
     cannot be retrieved afterwards** — persist it in a secret store immediately.
  3. A machine client then authenticates **as that technical user** by putting its
     ``username`` / ``password`` into a :class:`ClientConfig` together with the Keycloak fields.
     The SDK runs the one-time ROPC ``offline_access`` login, keeps a background-refreshed
     access token, and attaches ``Authorization: Bearer <jwt>`` to every gRPC call — so
     application code never touches a token.
  4. The technical user can do project-scoped **runtime** work (``detect_intent``,
     ``list_intents``, session management, …) but not administrative operations.

All four technical-user RPCs are exposed as high-level ``client.services.agents.*`` wrappers,
so the Keycloak bearer is attached automatically — application code never builds a token.

Prerequisites: a running CAI server with Keycloak enabled, an existing project (agent), and the
admin credentials below. Fill in the placeholders, then run::

    python examples/agents/create_and_use_project_technical_user.py
"""
import uuid

from loguru import logger as log

from ondewo.nlu.agent_pb2 import (
    CreateProjectTechnicalUserRequest,
    CreateProjectTechnicalUserResponse,
    DeleteProjectTechnicalUserRequest,
    ListProjectTechnicalUsersRequest,
    ListProjectTechnicalUsersResponse,
    RotateProjectTechnicalUserPasswordRequest,
    RotateProjectTechnicalUserPasswordResponse,
)
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.intent_pb2 import (
    ListIntentsRequest,
    ListIntentsResponse,
)
from ondewo.nlu.session_pb2 import (
    DetectIntentRequest,
    DetectIntentResponse,
    QueryInput,
    TextInput,
)

# --- Connection + Keycloak configuration (fill these in) -------------------------------------
HOST: str = 'localhost'
PORT: str = '50055'
USE_SECURE_CHANNEL: bool = False

KEYCLOAK_URL: str = 'https://<host>/auth'  # base URL, the part before /realms/<realm>
KEYCLOAK_REALM: str = 'ondewo-ccai-platform'
KEYCLOAK_CLIENT_ID: str = 'ondewo-nlu-cai-sdk-public'  # the public SDK client (no secret)

# An administrator / project-developer identity that may create technical users on the project
# (must hold PROJECT_DEVELOPER or PROJECT_ADMIN on it).
ADMIN_USER_NAME: str = 'admin@ondewo.com'
ADMIN_PASSWORD: str = '<admin-password>'

# The project (agent) that the technical user is scoped to.
PROJECT_UUID: str = '<project-uuid>'
LANGUAGE_CODE: str = 'en-US'


def build_keycloak_client(user_name: str, password: str) -> Client:
    """Build a bearer-authenticated NLU client for one identity via the Keycloak ROPC flow.

    Args:
        user_name (str):
            The Keycloak login / email of the identity to authenticate as.
        password (str):
            That identity's password.

    Returns:
        Client:
            A client that attaches an auto-refreshed ``Authorization: Bearer`` token to every
            call. Constructing it triggers the one-time offline-token login.
    """
    config: ClientConfig = ClientConfig(
        host=HOST,
        port=PORT,
        keycloak_url=KEYCLOAK_URL,
        realm=KEYCLOAK_REALM,
        client_id=KEYCLOAK_CLIENT_ID,
        user_name=user_name,
        password=password,
    )
    return Client(config=config, use_secure_channel=USE_SECURE_CHANNEL)


def main() -> None:
    parent: str = f'projects/{PROJECT_UUID}/agent'

    # 1) Authenticate as the admin / project-developer.
    admin_client: Client = build_keycloak_client(ADMIN_USER_NAME, ADMIN_PASSWORD)

    # 2) Create a project-scoped technical user. The password is returned ONCE.
    created: CreateProjectTechnicalUserResponse = admin_client.services.agents.create_project_technical_user(
        CreateProjectTechnicalUserRequest(parent=parent, name='sip-runtime'),
    )
    log.info(f"Created technical user: user_id={created.user_id} username={created.username}")
    log.warning('Store this password NOW — it is shown once and cannot be retrieved later.')
    technical_user_id: str = created.user_id
    technical_user_name: str = created.username
    technical_user_password: str = created.password  # persist securely (secret store / env var)

    # 3) List the project's technical users (usernames only — no passwords are returned).
    listed: ListProjectTechnicalUsersResponse = admin_client.services.agents.list_project_technical_users(
        ListProjectTechnicalUsersRequest(parent=parent),
    )
    for technical_user in listed.technical_users:
        log.info(
            f"  technical_user: {technical_user.username} "
            f"(id={technical_user.user_id}, created_by={technical_user.created_by})"
        )

    # 4) Authenticate AS the technical user and do runtime (PROJECT_EXECUTOR) work. A real
    #    machine client would read these credentials from its secret store, not from step 2.
    technical_user_client: Client = build_keycloak_client(technical_user_name, technical_user_password)

    #    a) detect_intent — the canonical runtime call (what sip/csi/vtsi use the technical user
    #       for). The high-level wrapper attaches the bearer automatically.
    session: str = f'{parent}/sessions/{uuid.uuid4()}'
    detect_response: DetectIntentResponse = technical_user_client.services.sessions.detect_intent(
        DetectIntentRequest(
            session=session,
            query_input=QueryInput(text=TextInput(text='hello', language_code=LANGUAGE_CODE)),
        ),
    )
    for message in detect_response.query_result.fulfillment_messages:
        log.info(f"bot: {list(message.text.text)}")

    #    b) a simple project-scoped read the technical user is allowed to perform.
    intents: ListIntentsResponse = technical_user_client.services.intents.list_intents(
        ListIntentsRequest(parent=parent, language_code=LANGUAGE_CODE),
    )
    log.info(f"Technical user can read {len(intents.intents)} intents in the project.")

    # 5) Lifecycle management (optional, shown for completeness — you would normally do these
    #    independently, not right after creating the user).
    #    Rotate the password: invalidates the old one and returns a new one ONCE.
    rotated: RotateProjectTechnicalUserPasswordResponse = (
        admin_client.services.agents.rotate_project_technical_user_password(
            RotateProjectTechnicalUserPasswordRequest(parent=parent, user_id=technical_user_id),
        )
    )
    log.info(f"Rotated password for {rotated.username}; update your secret store with the new value.")

    #    Delete the technical user when it is no longer needed (removes the Keycloak user and the
    #    project membership). After this it can no longer authenticate.
    admin_client.services.agents.delete_project_technical_user(
        DeleteProjectTechnicalUserRequest(parent=parent, user_id=technical_user_id),
    )
    log.info(f"Deleted technical user {technical_user_id}.")


if __name__ == '__main__':
    main()
