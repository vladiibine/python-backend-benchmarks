#!/bin/sh

gunicorn -b 0:8000 config.wsgi