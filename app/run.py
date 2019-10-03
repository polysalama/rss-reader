from tornado.ioloop import IOLoop
from tornado import web
from momoko.exceptions import PartiallyConnectedError
from time import sleep
import json
import momoko


def get_config():
    try:
        with open('./config/config.json') as config_file:
            config = json.load(config_file)
    except FileNotFoundError as error:
        print(error.strerror + ': ' + error.filename)
        exit(1)
    except OSError as error:
        print(error.strerror)
        exit(2)
    return config

class MainHandler(web.RequestHandler):
    def get(self):
        self.write('Hello, world')

def make_app():
    app = web.Application([(r'/', MainHandler)], **get_config())
    return app

def connect_to_db(app):
    i = 1
    while True:
        try:
            dns = (
            f'dbname={app.settings["db_name"]} '
            f'user={app.settings["db_user"]} '
            f'password={app.settings["db_password"]} '
            f'host={app.settings["db_host"]} '
            f'port={app.settings["db_port"]} '
            )
            app.db = momoko.Pool(dns, size=1, ioloop=IOLoop.current())
            IOLoop.current().run_sync(lambda: app.db.connect())
            break
        except PartiallyConnectedError as e:
            if i < 5:
                i = i + 1
                sleep(1)
                continue
            else:
                exit(1)

def create_tables(db):
    with open("schema.sql") as f:
            schema = f.read()
    db.execute(schema)

if __name__ == '__main__':
    app = make_app()
    connect_to_db(app)
    create_tables(app.db)
    app.listen(app.settings['port'])
    IOLoop.current().start()