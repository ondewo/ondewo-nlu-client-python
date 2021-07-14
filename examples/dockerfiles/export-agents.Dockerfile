FROM registry-dev.ondewo.com:5000/ondewo/python:3.8-slim-buster

RUN apt-get update && apt-get install -y git

COPY export src

WORKDIR src

ARG REQUIREMENTS_FILE_NAME=requirements-export-agents.txt
RUN pip install -r $REQUIREMENTS_FILE_NAME

# --config="$(cat <dir>/conf.json)" --exported-agents-dir-name=2.6.x --secure
ENTRYPOINT ["python", "-m" ,"export"]