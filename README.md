<div align="center">
  <table>
    <tr>
      <td>
        <a href="https://ondewo.com/en/products/natural-language-understanding/">
            <img width="400px" src="https://raw.githubusercontent.com/ondewo/ondewo-logos/master/ondewo_we_automate_your_phone_calls.png"/>
        </a>
      </td>
    </tr>
    <tr>
        <td align="center">
          <a href="https://www.linkedin.com/company/ondewo "><img width="40px" src="https://cdn-icons-png.flaticon.com/512/3536/3536505.png"></a>
          <a href="https://www.facebook.com/ondewo"><img width="40px" src="https://cdn-icons-png.flaticon.com/512/733/733547.png"></a>
          <a href="https://twitter.com/ondewo"><img width="40px" src="https://cdn-icons-png.flaticon.com/512/733/733579.png"> </a>
          <a href="https://www.instagram.com/ondewo.ai/"><img width="40px" src="https://cdn-icons-png.flaticon.com/512/174/174855.png"></a>
        </td>
    </tr>
  </table>
  <h1>
  Ondewo NLU Client Python Library
  </h1>
</div>

This library facilitates the interaction between a user and a CAI server. It achieves this by providing a higher-level interface mediator.

This higher-level interface mediator is structured around a series of python files generated from protobuf files. These protobuf files specify the details of the interface, and can be used to generate code in 10+ high-level languages. They are found in the [ONDEWO NLU API](https://github.com/ondewo/ondewo-nlu-api) along with the older Google protobufs from Dialogueflow that were used at the start. The [ONDEWO PROTO-COMPILER](https://github.com/ondewo/ondewo-proto-compiler) will generate the needed files directly in this library.

## Python Installation

You can install the library by installing it directly from the PyPi:

```bash
pip install ondewo-nlu-client
```

Or, you could clone it and install the requirements:

```bash
git clone git@github.com:ondewo/ondewo-nlu-client-python.git
cd ondewo-nlu-client-python
make setup_developer_environment_locally
```

## Repository Structure

```
.
├── examples                         <----- Helpful for implementation of code
├── ondewo
│   ├── nlu
│   │   ├── convenience
│   │   │   ├── __init__.py
│   │   │   └── shared_request_data.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── services_container.py
│   │   │   └── services_interface.py
│   │   ├── scripts
│   │   │   ├── client_example_script.py
│   │   │   └── __init__.py
│   │   ├── services
│   │   │   ├── agents.py
│   │   │   ├── aiservices.py
│   │   │   ├── async_agents.py
│   │   │   ├── async_aiservices.py
│   │   │   ├── ...
│   │   │   ├── __init__.py
│   │   │   ├── ...
│   │   ├── utils
│   │   │   ├── __init__.py
│   │   │   └── login.py
│   │   ├── agent_pb2_grpc.py
│   │   ├── agent_pb2.py
│   │   ├── agent_pb2.pyi
│   │   ├── aiservices_pb2_grpc.py
│   │   ├── aiservices_pb2.py
│   │   ├── aiservices_pb2.pyi
│   │   ├── ...
│   ├── qa
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── services_container.py
│   │   │   └── services_interface.py
│   │   ├── services
│   │   │   ├── __init__.py
│   │   │   └── qa.py
│   │   ├── client_config.py
│   │   ├── client.py
│   │   ├── __init__.py
│   │   ├── py.typed
│   │   ├── qa_pb2_grpc.py
│   │   ├── qa_pb2.py
│   │   └── qa_pb2.pyi
│   └── __init__.py
├── ondewo-nlu-api                         <----- @ https://github.com/ondewo/ondewo-nlu-api
├── ondewo-proto-compiler                  <----- @ https://github.com/ondewo/ondewo-proto-compiler
├── CONTRIBUTING.md
├── Dockerfile
├── Dockerfile.utils
├── LICENSE
├── Makefile
├── MANIFEST.in
├── mypy.ini
├── README.md
├── RELEASE.md
├── requirements-dev.txt
├── requirements.txt
├── setup.cfg
└── setup.py
```

## Build

The `make build` command is dependent on 2 `repositories` and their speciefied `version`:

- [ondewo-nlu-api](https://github.com/ondewo/ondewo-nlu-api) -- `NLU_API_GIT_BRANCH` in `Makefile`
- [ondewo-proto-compiler](https://github.com/ondewo/ondewo-proto-compiler) -- `ONDEWO_PROTO_COMPILER_GIT_BRANCH` in `Makefile`

It will generate a `_pb2.py`, `_pb2.pyi` and `_pb2_grpc.py` file for every `.proto` in the api submodule.

> :warning: All Files in the `ondewo` folder that dont have `pb2` in their name are handwritten, and therefor need to be manually adjusted to any changes in the proto-code.

## Adding Convenience Methods

The `_pb2_grpc.py` stubs expose every RPC as a raw method that requires the caller to construct gRPC metadata manually and handle channel lifecycle. The service wrappers in `ondewo/nlu/services/` sit on top of those stubs and handle the boilerplate (auth token injection via `self.metadata`, channel creation via `self.grpc_channel`) so that application code stays clean.

Without a convenience method a caller would write:

```python
import grpc
from ondewo.nlu.rag_pb2 import RagAskRequest
from ondewo.nlu.rag_pb2_grpc import RagsStub

channel = grpc.secure_channel("host:port", grpc.ssl_channel_credentials())
stub = RagsStub(channel)
metadata = [("authorization", "Bearer <token>")]
for chunk in stub.RagAsk(RagAskRequest(query="hello"), metadata=metadata):
    print(chunk)
```

With a convenience method via `Client` or `AsyncClient` the same call becomes:

```python
# Synchronous
from ondewo.nlu.client import Client
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.rag_pb2 import RagAskRequest

client = Client(config=ClientConfig(host="host", port=1234, ...), use_secure_channel=True)
for chunk in client.services.rags.rag_ask(RagAskRequest(query="hello")):
    print(chunk)
```

```python
# Asynchronous
import asyncio
from ondewo.nlu.async_client import AsyncClient
from ondewo.nlu.client_config import ClientConfig
from ondewo.nlu.rag_pb2 import RagAskRequest

async def main() -> None:
    client = AsyncClient(config=ClientConfig(host="host", port=1234, ...), use_secure_channel=True)
    async for chunk in await client.services.rags.rag_ask(RagAskRequest(query="hello")):
        print(chunk)

asyncio.run(main())
```

To add a new service manually, follow the four steps below.

### 1. Write the sync service file

Create `ondewo/nlu/services/my_services.py` (use a pluralized name matching the proto service name, e.g. `service Rags` → `rags.py`). Subclass `ServicesInterface`, define a `stub` property, and add one method per RPC.

Rules to follow:

- Method names are the snake_case version of the PascalCase RPC name (e.g. `RagAsk` → `rag_ask`).
- For unary RPCs: `request` is a single protobuf message and the return type is a single protobuf message.
- For **client-streaming** RPCs: `request` is `Iterator[MyRequest]`.
- For **server-streaming** RPCs: the return type is `Iterator[MyResponse]` and the response must **not** be `await`-ed.
- Import `Empty` from `google.protobuf.empty_pb2` and `Operation` from `ondewo.nlu.operations_pb2`.

```python
from typing import Iterator

from google.protobuf.empty_pb2 import Empty

from ondewo.nlu.my_service_pb2 import (
    MyCreateRequest,
    MyCreateResponse,
    MyListRequest,
    MyListResponse,
    MyStreamRequest,
    MyStreamResponse,
)
from ondewo.nlu.my_service_pb2_grpc import MyServicesStub
from ondewo.nlu.core.services_interface import ServicesInterface


class MyServices(ServicesInterface):
    """Exposes the MyService endpoints of ONDEWO NLU in a user-friendly way."""

    @property
    def stub(self) -> MyServicesStub:
        stub: MyServicesStub = MyServicesStub(channel=self.grpc_channel)
        return stub

    # Unary RPC
    def my_create(self, request: MyCreateRequest) -> MyCreateResponse:
        response: MyCreateResponse = self.stub.MyCreate(request, metadata=self.metadata)
        return response

    # Client-streaming RPC
    def my_upload(self, request: Iterator[MyCreateRequest]) -> MyCreateResponse:
        response: MyCreateResponse = self.stub.MyUpload(request, metadata=self.metadata)
        return response

    # Server-streaming RPC
    def my_stream(self, request: MyStreamRequest) -> Iterator[MyStreamResponse]:
        response: Iterator[MyStreamResponse] = self.stub.MyStream(request, metadata=self.metadata)
        return response
```

### 2. Write the async service file

Create `ondewo/nlu/services/async_my_services.py`. The structure mirrors the sync file with three differences:

- Subclass `AsyncServicesInterface` (imported from `ondewo.nlu.core.async_services_interface`).
- All methods are `async def`.
- Unary and client-streaming methods `await` the stub call. Server-streaming methods do **not** use `await`.

```python
from typing import AsyncIterator, Iterator

from google.protobuf.empty_pb2 import Empty

from ondewo.nlu.my_service_pb2 import (
    MyCreateRequest,
    MyCreateResponse,
    MyStreamRequest,
    MyStreamResponse,
)
from ondewo.nlu.my_service_pb2_grpc import MyServicesStub
from ondewo.nlu.core.async_services_interface import AsyncServicesInterface


class MyServices(AsyncServicesInterface):
    """Exposes the MyService endpoints of ONDEWO NLU in a user-friendly way."""

    @property
    def stub(self) -> MyServicesStub:
        stub: MyServicesStub = MyServicesStub(channel=self.grpc_channel)
        return stub

    # Unary RPC
    async def my_create(self, request: MyCreateRequest) -> MyCreateResponse:
        response: MyCreateResponse = await self.stub.MyCreate(request, metadata=self.metadata)
        return response

    # Client-streaming RPC
    async def my_upload(self, request: Iterator[MyCreateRequest]) -> MyCreateResponse:
        response: MyCreateResponse = await self.stub.MyUpload(request, metadata=self.metadata)
        return response

    # Server-streaming RPC — no await
    async def my_stream(self, request: MyStreamRequest) -> AsyncIterator[MyStreamResponse]:
        response: AsyncIterator[MyStreamResponse] = self.stub.MyStream(request, metadata=self.metadata)
        return response
```

### 3. Register the new service in the containers

**`ondewo/nlu/core/services_container.py`** — import the sync class and add a typed field:

```python
from ondewo.nlu.services.my_services import MyServices

@dataclass
class ServicesContainer(BaseServicesContainer):
    ...
    my_services: MyServices
```

**`ondewo/nlu/core/async_services_container.py`** — import the async class and add a typed field:

```python
from ondewo.nlu.services.async_my_services import MyServices

@dataclass
class AsyncServicesContainer(BaseServicesContainer):
    ...
    my_services: MyServices
```

> **Note:** `ServicesContainer` and `AsyncServicesContainer` are plain dataclasses with no default values, so omitting any field will raise a `TypeError` at runtime.

### 4. Instantiate the service in the clients

**`ondewo/nlu/client.py`** — import the sync class and pass an instance to `ServicesContainer`:

```python
from ondewo.nlu.services.my_services import MyServices

self.services = ServicesContainer(
    ...
    my_services=MyServices(**kwargs),
)
```

**`ondewo/nlu/async_client.py`** — import the async class and pass an instance to `AsyncServicesContainer`:

```python
from ondewo.nlu.services.async_my_services import MyServices

self.services = AsyncServicesContainer(
    ...
    my_services=MyServices(**kwargs),
)
```

---

## Examples

The `/examples` folder provides a possible implementation of this library. To run an example, simple execute it like any other python file. To specify the server and credentials, you need to provide an environment file with the following variables:

- host `// The hostname of the Server - e.g. 127.0.0.1`
- port `// Port of the Server - e.g. 6600`
- user_name `// Username - same as you would use in AIM`
- password `// Password of the user`
- http_token `// Token to allow access through`
- grpc_cert `// gRPC Certificate of the server`

## Automatic Release Process

The entire process is automated to make development easier. The actual steps are simple:

TODO after Pull Request was merged in:

- Checkout master:

  ```shell
  git checkout master
  ```

- Pull the new stuff:

  ```shell
  git pull
  ```

- (If not already, run the `setup_developer_environment_locally` command):

  ```shell
  make setup_developer_environment_locally
  ```

- Update the `ONDEWO_NLU_VERSION` in the `Makefile`
- Add the new Release Notes in `RELEASE.md` in the format:

  ``` markdown
  ## Release ONDEWO NLU Python Client X.X.X       <---- Beginning of Notes

     ...<NOTES>...

  *****************                      <---- End of Notes
  ```

- Release:

  ```shell
  make ondewo_release
  ```

---

The release process can be divided into 6 Steps:

1. `build` specified version of the `ondewo-nlu-api`
2. `commit and push` all changes in code resulting from the `build`
3. Create and push the `release branch` e.g. `release/1.3.20`
4. Create and push the `release tag` e.g. `1.3.20`
5. Create a new `Release` on GitHub
6. Publish the built `dist` folder to `pypi.org`

> :warning: The Release Automation checks if the build has created all the proto-code files, but it does not check the code-integrity. Please build and test the generated code prior to starting the release process.
