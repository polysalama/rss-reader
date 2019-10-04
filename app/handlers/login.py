from tornado import web

class MainHandler(web.RequestHandler):
    def get(self):
        self.render('index.html')