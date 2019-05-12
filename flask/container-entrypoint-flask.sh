#!/bin/sh

gunicorn -b 0:8000 flask_app:app