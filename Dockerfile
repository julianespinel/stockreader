FROM ubuntu:latest
MAINTAINER Julian Espinel "julianespinel@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /stockboard
WORKDIR /stockboard
RUN pip3 install -r requirements.txt
