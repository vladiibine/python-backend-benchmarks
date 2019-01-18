FROM python:3.7.1-alpine

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

COPY requirements_database_setup.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

