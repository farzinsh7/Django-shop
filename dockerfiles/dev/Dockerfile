FROM python:3.10-slim-buster

LABEL maintainer="farzinweb@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY ./requirements.txt .

RUN pip instal --upgrade pip && pip instal -r requirements.txt

COPY ./core .