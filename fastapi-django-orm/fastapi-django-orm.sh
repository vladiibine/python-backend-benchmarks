#!/bin/sh

python -m uvicorn fastapi_django_app:app --host 0 --port 8000 --log-level warning