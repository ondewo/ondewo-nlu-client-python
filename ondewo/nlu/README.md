Ondewo Python Client
====================
This module provides a python client for convenient interaction between a user and his/her ONDEWO NLU server.

Quick Introduction
------------------
1. Instantiate a client: This logs the user in with the login-information provided via the client config.
    ```python
    from ondewo.nlu.client import Client
    from ondewo.nlu.client_config import ClientConfig

    config = ClientConfig(
        host='my_host',
        port='my_port',
        http_token='my_http_token', # the token required for getting past nginx
        grpc_cert=b'my_certificate', # the certificate required for setting up a secure grpc channel
        user_name='user@ondewo.com', # the user name for ONDEWO NLU services
        password='1234', # the password for ONDEWO NLU services
    )

    client = Client(config=config)
    ```
   Note: Since a login is necessary, any intermediate service rerouting requests to an ONDEWO NLU server
    must at least make the Login endpoint available to the client.

   Note: By default, a secure grpc-channel is established.
    If the backend allows, you can use an insecure channel by
    instantiating a client using `client = Client(config=config, use_secure_channel=False)`.
    In this case, the `grpc_cert` field can be left empty. Otherwise, this will throw an error.

1. Discover all available services by tab-completion on `client.services.`.
    E.g., `client.services.sessions` for sessions-related functionality or `client.services.contexts` for contexts-related functionality.

1. Interact with one of the endpoints exposed by the services, e.g., the DetectIntent endpoint.
    ```python
    from google.cloud.dialogflow.v2.session_pb2 import DetectIntentRequest, DetectIntentResponse

    request: DetectIntentRequest = DetectIntentRequest
    request.query_input.text.text = 'Hello Agent'
    request.query_input.text.language_code = 'en'
    request.session = 'project/project_ID/agent/sessions/session_ID'
    response: DetectIntentResponse = client.services.sessions.detect_intent(request)
    print(response.query_result.intent.display_name)
    ```

1. Play with the example script at `ondewo_client/python/scripts/client_example_script.py` to find out more or continue to read.

Client configuration
--------------------
The client configuration controls which NLU server we are interacting with and the user used for this interaction.
To log in a new user or connect to a different server, create a new client config and instantiate a new client.

```python
new_config = ClientConfig(
    host='my_new_host',
    port='my_new_port',
    http_token='my_new_http_token', # the token required for getting past nginx
    grpc_cert=b'my_new_certificate', # the certificate required for setting up a secure grpc channel
    user_name='new_user@ondewo.com', # the user name for ONDEWO NLU services
    password='new_password', # the password for ONDEWO NLU services
)

new_client = Client(config=new_config)
```

Conventions
-----------
The client uses the names of the grpc services and endpoints but in snake_case to conform to Python style conventions.

Example:

- grpc Endoint: Sessions ==> client.services.sessions

- Endpoint method: Sessions.DetectIntent ==> client.services.sessions.detect_intent

The signatures of the endpoint methods are exactly the same as the signatures of grpc services as described in the proto files.

Example:

- grpc Service
```python
class Sessions(...):
    def DetectIntent(self, request: DetectIntentRequest) -> DetectIntentResponse:
```

- corresponding client method
```python
client.services.sessions.detect_intent # type: Callable[[DetectIntentRequest], DetectIntentResponse]
```

Convenience methods for development
===================================

Working with incomplete requests: SharedRequestData.fill_missing_fields()
-------------------------------------------------------------------------

The requests to be sent to the NLU backend can be quite complex.
To simplify life, we provide a **helper dataclass SharedRequestData** which can

- _hold information which is typically the same across many requests_ (e.g., language_code, session_id, etc)

- _provides a method fill_missing_fields to fill unset fields on a request_ using this information


Example:
```python
from ondewo.nlu.convenience import SharedRequestData
from google.cloud.dialogflow.v2.session_pb2 import DetectIntentRequest, DetectIntentResponse
shared_request_data = SharedRequestData(
        project_parent='project/id/agent',
        session_uuid="17531756-a428-4290-8699-4d46c995fe44",
        language_code='en',
    )

request: DetectIntentRequest = DetectIntentRequest
request.query_input.text.text = 'Hello Agent'
request = shared_request_data.fill_missing_fields(request)  # fill missing fields in request from shared_request_data

response: DetectIntentResponse = client.services.sessions.detect_intent(request)
print(response.query_result.intent.display_name)
```
Note that we did not need to explicitly set all fields on this request:
request.session and request.query_input.text.language_code, for example, were filled from shared_request_data.

Play with the example script at `ondewo_client/python/scripts/client_example_script.py`
(section `### CONVENIENCE: share request data among different request types` and below) to find out more or continue to read.
