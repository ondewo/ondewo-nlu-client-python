FROM python:3.12-slim

ENV LANG=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Vienna

RUN apt-get update -qq && \
  apt-get dist-upgrade -qq -y --no-install-recommends --fix-missing libgmp10 libssl-dev libpcre3-dev build-essential tk-dev tzdata && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
  echo $TZ > /etc/timezone && \
  dpkg-reconfigure --frontend noninteractive tzdata && \
  apt-get clean && apt-get purge -y --auto-remove \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /home/ondewo/

# Install the client library (runtime dependencies resolved from pyproject.toml
# by the setuptools backend) into the system environment.
COPY pyproject.toml README.md ./
COPY ondewo ondewo
COPY examples examples
RUN uv pip install --system .
