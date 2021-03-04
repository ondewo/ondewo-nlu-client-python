Ondewo Client Library
======================

This library facilitates the interaction between a user and his/her CAI server. It achieves this by providing a higher-level interface mediator.

This higher-level interface mediator is structured around a series of python files genereted from protobuff files. These protobuf files specify the details of the interface, and can be used to generate code in 10+ high-level languages. They are found in the [apis submodule](./ondewo-nlu-api) along with the older Google protobufs from Dialogueflow that were used at the start.

Python Installation
-------------------
You can install the library by installing it directly from the repository:
```bash
pip install -e https://github.com/ondewo/ondewo-nlu-client-python#egg=ondewo_client
```

Or, you could clone it and install the requirements:
```bash
git clone git@github.com:ondewo/ondewo-nlu-client-python.git
cd ondewo-client
pip install -r requirements/python-requirements.txt
```

Let's Get Started! (WIP)
------------------
Import your programming interface:
```bash
ls ondewo
```

Get a suitable example:
```bash
ls examples
```
