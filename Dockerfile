FROM python:3.10-slim-buster

COPY requirements.txt /temp/requirements.txt
RUN python -m pip install -U pip

RUN apt-get update \ 
    && apt-get -y install libpq-dev gcc
RUN pip install -r /temp/requirements.txt
COPY djangoshop /djangoshop
WORKDIR /djangoshop
EXPOSE 8000

RUN adduser --disabled-password djangoshop-user

USER djangoshop-user