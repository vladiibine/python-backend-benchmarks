#!/bin/sh

/app/benchmark_dj/manage.py migrate
/app/benchmark_dj/manage.py runserver 0:8000