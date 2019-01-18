#!/bin/sh

/app/db_init/manage.py migrate
tail -f /dev/null