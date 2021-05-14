FROM python:3.9

COPY requirements_fastapi-sqlalchemy-async.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app
