<p align="center">
    <a href="https://www.ondewo.com">
      <img alt="ONDEWO Logo" src="https://raw.githubusercontent.com/ondewo/ondewo-logos/master/github/ondewo_logo_github_2.png"/>
    </a>
</p>


## Ondewo NLU Client Python Library

This library facilitates the interaction between a user and a CAI server. It achieves this by providing a higher-level interface mediator.

This higher-level interface mediator is structured around a series of python files generated from protobuf files. These protobuf files specify the details of the interface, and can be used to generate code in 10+ high-level languages. They are found in the [apis submodule](./ondewo-nlu-api) along with the older Google protobufs from Dialogueflow that were used at the start.

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
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   ├── services_container.cpython-38.pyc
│   │   │   │   └── services_interface.cpython-38.pyc
│   │   │   ├── __init__.py
│   │   │   ├── services_container.py
│   │   │   └── services_interface.py
│   │   ├── __pycache__
│   │   │   ├── agent_pb2.cpython-38.pyc
│   │   │   ├── agent_pb2_grpc.cpython-38.pyc
│   │   │   ├── ...
│   │   ├── scripts
│   │   │   ├── client_example_script.py
│   │   │   └── __init__.py
│   │   ├── services
│   │   │   ├── __pycache__
│   │   │   │   ├── agents.cpython-38.pyc
│   │   │   │   ├── aiservices.cpython-38.pyc
│   │   │   │   ├── contexts.cpython-38.pyc
│   │   │   │   ├── entity_types.cpython-38.pyc
│   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   ├── intents.cpython-38.pyc
│   │   │   │   ├── operations.cpython-38.pyc
│   │   │   │   ├── project_roles.cpython-38.pyc
│   │   │   │   ├── project_statistics.cpython-38.pyc
│   │   │   │   ├── server_statistics.cpython-38.pyc
│   │   │   │   ├── sessions.cpython-38.pyc
│   │   │   │   ├── users.cpython-38.pyc
│   │   │   │   └── utilities.cpython-38.pyc
│   │   │   ├── agents.py
│   │   │   ├── aiservices.py
│   │   │   ├── contexts.py
│   │   │   ├── entity_types.py
│   │   │   ├── __init__.py
│   │   │   ├── intents.py
│   │   │   ├── operations.py
│   │   │   ├── project_roles.py
│   │   │   ├── project_statistics.py
│   │   │   ├── server_statistics.py
│   │   │   ├── sessions.py
│   │   │   ├── users.py
│   │   │   └── utilities.py
│   │   ├── utils
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   └── login.cpython-38.pyc
│   │   │   ├── __init__.py
│   │   │   └── login.py
│   │   ├── agent_pb2_grpc.py
│   │   ├── agent_pb2.py
│   │   ├── agent_pb2.pyi
│   │   ├── aiservices_pb2_grpc.py
│   │   ├── aiservices_pb2.py
│   │   ├── aiservices_pb2.pyi
│   │   ├── ...
│   ├── __pycache__
│   │   └── __init__.cpython-38.pyc
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

## Examples

The `/examples` folder provides a possible implementation of this library. To run an example, simple execute it like any other python file. To specify the server and credentials, you need to provide an environment file with the following variables:
- host         `// The hostname of the Server - e.g. 127.0.0.1`
- port         `// Port of the Server - e.g. 6600`
- user_name    `// Username - same as you would use in AIM`
- password     `// Password of the user`
- http_token   `// Token to allow access through`
- grpc_cert    `// gRPC Certificate of the server`

## Automatic Release Process

The entire process is automated to make development easier. The actual steps are simple:

==TODO== after Pull Request was merged in:

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
   ```
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

> :warning:  The Release Automation checks if the build has created all the proto-code files, but it does not check the code-integrity. Please build and test the generated code prior to starting the release process.
