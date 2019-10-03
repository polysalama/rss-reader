import tornado.ioloop
import tornado.web
import json

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

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app(config):
    return tornado.web.Application([
        (r"/", MainHandler),
    ], **config)

if __name__ == "__main__":
    config = get_config()
    app = make_app(config)
    app.listen(config["port"])
    tornado.ioloop.IOLoop.current().start()