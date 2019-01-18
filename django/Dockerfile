FROM python:3.7.1-alpine

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app

#RUN ./benchmark_dj/manage.py migrate

#CMD [".//manage.py runserver 0:8000"]