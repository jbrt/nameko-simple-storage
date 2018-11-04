FROM python:3.6.7-alpine3.8

MAINTAINER Julien B. (http://github.com/jbrt)

ENV NAMEKO_HOME /nameko

COPY . ./$NAMEKO_HOME

RUN apk add --no-cache gcc make libc-dev libffi-dev libressl-dev
RUN pip install --no-cache -r /$NAMEKO_HOME/requirements.txt

WORKDIR /$NAMEKO_HOME/nameko-simple-storage

ENTRYPOINT nameko run service --config ../config.yml