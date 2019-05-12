import os

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado import web

import momoko


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class OneQueryHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        cur = yield self.db.execute('SELECT COUNT(*) FROM auth_permission;')
        result = cur.fetchone()
        cur.close()
        self.write(f"{result[0]}")
        self.finish()


class TenQueriesSerialHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        counter = 0

        for _ in range(10):
            cur = yield self.db.execute('SELECT COUNT(*) FROM auth_permission;')
            result = cur.fetchone()
            counter += result[0]
            cur.close()

        self.write(f"{counter}")
        self.finish()


if __name__ == '__main__':
    parse_command_line()
    application = web.Application([
        (r'/1q/', OneQueryHandler),
        (r'/10q/', TenQueriesSerialHandler),
    ])

    ioloop = IOLoop.instance()
    database = os.environ['POSTGRES_DB']
    user = os.environ['POSTGRES_USER']
    password = os.environ['POSTGRES_PASSWORD']
    host = os.environ['POSTGRES_HOST']

    application.db = momoko.Pool(
        dsn='dbname={} user={} password={} host={}'
            .format(database, user, password, host),
        size=1,
        ioloop=ioloop,
    )

    # this is a one way to run ioloop in sync
    future = application.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    http_server = HTTPServer(application)
    http_server.listen(8000)
    ioloop.start()
