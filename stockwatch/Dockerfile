FROM python:3.12-alpine

WORKDIR /usr/src/app

ENV pythonbuffered=1
ENV pythonwritebytecode=1

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN python -m pip install -r /usr/src/app/requirements.txt

COPY . /usr/src/app
