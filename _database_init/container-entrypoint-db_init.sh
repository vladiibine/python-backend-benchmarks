#!/bin/sh

/app/benchmark_dj/manage.py migrate
tail -f /dev/null