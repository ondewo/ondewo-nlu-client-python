FROM python:3.8-slim

RUN apt-get update && \
	apt-get purge -y --auto-remove

WORKDIR /home/ondewo/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ondewo ondewo
COPY examples examples
