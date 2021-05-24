FROM python:3.9

COPY requirements_fastapi-django-orm.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY . /app
WORKDIR /app
