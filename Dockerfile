FROM python:3.10-alpine3.17

COPY requirements.txt /temp/requirements.txt
COPY djangoshop /djangoshop
WORKDIR /djangoshop
EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password djangoshop-user

USER djangoshop-user