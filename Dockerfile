FROM python:3.8-slim

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

WORKDIR /home/ondewo/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ondewo ondewo
COPY examples examples
