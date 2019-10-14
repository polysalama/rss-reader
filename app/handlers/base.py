from tornado import web
class BaseHandler(web.RequestHandler):
    # Base class for all handlers

    def get_current_user(self):
        return self.get_secure_cookie("user_id")