FROM python:3.7-slim

ENV PYTHONUNBUFFERED 1

RUN apt update && apt-get install -y \
    # libffi-dev \
    # gettext \
    # git \
    # python3-dev \
    libpq-dev \
    gcc
    # python3-psycopg2

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . /code/