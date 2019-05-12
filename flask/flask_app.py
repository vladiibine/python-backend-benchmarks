import os

from flask import Flask
from psycopg2 import connect

app = Flask(__name__)

@app.route("/1q/")
def one_query_sequential():
    database = os.environ['POSTGRES_DB']
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']

    dsn='dbname={} user={} password={} host={}'.format(
        database, user, password, host)

    with connect(dsn=dsn) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT COUNT(*) FROM auth_permission;')

        res = cursor.fetchone()

        return str(res[0])
