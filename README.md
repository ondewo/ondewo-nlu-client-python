<p align="center">
    <a href="https://www.ondewo.com">
      <img alt="ONDEWO Logo" src="https://raw.githubusercontent.com/ondewo/ondewo-logos/master/github/ondewo_logo_github_2.png"/>
    </a>
</p>

Ondewo NLU Client Library
======================

This library facilitates the interaction between a user and his/her CAI server. It achieves this by providing a higher-level interface mediator.

This higher-level interface mediator is structured around a series of python files genereted from protobuff files. These protobuf files specify the details of the interface, and can be used to generate code in 10+ high-level languages. They are found in the [apis submodule](./ondewo-nlu-api) along with the older Google protobufs from Dialogueflow that were used at the start.

Python Installation
-------------------
You can install the library by installing it directly from the pypi:
```bash
pip install ondewo-nlu-client
```

Or, you could clone it and install the requirements:
```bash
git clone git@github.com:ondewo/ondewo-nlu-client-python.git
cd ondewo-nlu-client-python
pip install -e .
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
Automatic Release Process
------------------
The entire process is automated to make development easier. The actual steps are simple:

TODOs in Pull Request before the release:

 - Update the Version number inside the Makefile
   - ! : Major and Minor Version Number must be the same for Client and API at all times
      >example: API 2.9.0 --> Client 2.9.X

 - Check if RELEASE.md is up-to-date

 - Update the Version number inside the setup.py by using:
    ```bash
    make update_setup
    ```

TODOs after Pull Request was merged in:

 - Checkout master:
    ```bash
    git checkout master
    ```
 - Pull the new stuff:
    ```bash
    git pull
    ```
 - Release:
    ```bash
    make ondewo_release
    ```

The   ``` make ondewo_release``` command can be divided into 5 steps:

- cloning the devops-accounts repository and extracting the credentials
- creating and pushing the release branch
- creating and pushing the release tag
- creating the GitHub release
- creating and pushing the new PyPi release

The variables for the GitHub Access Token, PyPi Username and Password are all inside
of the Makefile, but the values are overwritten during ``` make ondewo_release```, because
they are passed from the devops-accounts repo as arguments to the actual ```release``` command.
