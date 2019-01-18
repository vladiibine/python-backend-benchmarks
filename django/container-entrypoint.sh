#!/bin/sh

/app/benchmark_dj/manage.py migrate
gunicorn -b 0:8000 config.wsgi