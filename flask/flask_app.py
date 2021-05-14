import logging
import os

from flask import Flask
from psycopg2 import connect

app = Flask(__name__)
database = os.environ['POSTGRES_DB']
user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']

dsn = 'dbname={} user={} password={} host={}'.format(
    database, user, password, host)
connection = connect(dsn=dsn)

logging.getLogger("web").handlers = []


@app.route("/1q/")
def one_query_sequential():

    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM auth_permission;')

    res = cursor.fetchone()

    return str(res[0])


@app.route("/10q/")
def ten_queries_sequential():
    cursor = connection.cursor()

    counter = 0

    for _ in range(10):
        cursor.execute('SELECT COUNT(*) FROM auth_permission;')

        res = cursor.fetchone()
        counter += res[0]

    return str(counter)
