#!/bin/sh

python -m uvicorn fastapi_app:app --host 0 --port 8000