from tornado import web
from tornado.ioloop import IOLoop
from .base import BaseHandler
import bcrypt

class LoginHandler(BaseHandler):
    async def get(self):
        if self.current_user:
            self.redirect('/rss_reader')
        else:
            self.render('index.html')

    async def post(self):
        sql = 'SELECT password FROM users WHERE email=%s'
        email = self.get_body_argument('email')
        input_password = self.get_body_argument('password').encode()
        cursor = await self.application.db.execute(sql, [email])
        hashed_password = cursor.fetchone()
        if hashed_password is None:
            self.write('No such user!')
            return
        check_password = await IOLoop.current().run_in_executor(None, 
                lambda: bcrypt.checkpw(input_password, 
                                       hashed_password[0].tobytes()))   
        if check_password:
            print(self.settings, flush=True) 
            self.set_secure_cookie("user", email)
            self.redirect('/rss_reader')
        else:
            self.write('Wrong password')
