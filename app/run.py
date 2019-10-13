from tornado.ioloop import IOLoop
from tornado import web
from momoko.exceptions import PartiallyConnectedError
from time import sleep
import json
import momoko
import aioredis
from handlers import login, register, rss_reader
from daos.dao import Dao


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
    config['template_path'] = './templates'
    config['login_url'] = '/login'
    return config

class Application(web.Application):
    def __init__(self, **settings):
        self.redis = None
        super(Application, self).__init__(**settings)

def connect_to_redis(app):
    app.redis = IOLoop.current() \
                .run_sync(lambda: aioredis \
                .create_redis_pool(f'redis://{app.settings["redis_host"]}:{app.settings["redis_port"]}'))

def make_app():
    app = web.Application([(r'/', login.RedirectHandler),
                           (r'/login', login.LoginHandler),
                           (r'/logout', login.LogoutHandler),
                           (r'/register', register.RegisterHandler),
                           (r'/rss_reader', rss_reader.RssHandler),
                           (r'/register_ok', register.RegisterSuccessHandler)],
                           **get_config())
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
            Dao.DB = app.db
            break
        except PartiallyConnectedError as e:
            if i < 5:
                i = i + 1
                sleep(1)
                continue
            else:
                exit(1)

def create_tables(db):
    with open('schema.sql') as f:
            schema = f.read()
    db.execute(schema)

def run_debug_smtp():
    from aiosmtpd.smtp import SMTP
    from aiosmtpd.controller import Controller

    class DebugHandler:
        async def handle_DATA(self, server, session, envelope):
            print('Message from %s' % envelope.mail_from)
            print('Message for %s' % envelope.rcpt_tos)
            print('Message data:\n')
            print(envelope.content.decode('utf8', errors='replace'), flush=True)
            print('End of message')
            return '250 Message accepted for delivery'

    controller = Controller(DebugHandler(), hostname='0.0.0.0', port=1025)
    controller.start()

if __name__ == '__main__':
    app = make_app()
    connect_to_db(app)
    create_tables(app.db)
    connect_to_redis(app)
    app.listen(app.settings['port'])
    if app.settings['debug']:
        run_debug_smtp()
    IOLoop.current().start()
