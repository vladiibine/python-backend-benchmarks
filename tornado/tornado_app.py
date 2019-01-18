from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado import web

import psycopg2
import momoko


class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class TutorialHandler(BaseHandler):
    @gen.coroutine
    def get(self):
        # self.write('Some text here!')
        cur = yield self.db.execute('SELECT COUNT(*) FROM auth_permission;')
        result = cur.fetchone()
        self.write(f"{result[0]}")
        self.finish()


if __name__ == '__main__' and 1 == 0:
    parse_command_line()
    application = web.Application([
        (r'/', TutorialHandler)
    ], debug=True)

    ioloop = IOLoop.instance()

    application.db = momoko.Pool(
        dsn='dbname=database user=user password=password host=database',
        size=1,
        ioloop=ioloop,
    )

    # this is a one way to run ioloop in sync
    future = application.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    http_server = HTTPServer(application)
    http_server.listen(8000, 'localhost')
    ioloop.start()


import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        cur = yield db.execute('SELECT COUNT(*) FROM auth_permission;')
        result = cur.fetchone()
        self.write(f"{result[0]}")
        self.finish()


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


if __name__ == "__main__":
    app = make_app()

    ioloop = IOLoop.instance()

    db = momoko.Pool(
        dsn='dbname=database user=user password=password host=database',
        size=1,
        ioloop=ioloop,
    )

    # this is a one way to run ioloop in sync
    future = db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
