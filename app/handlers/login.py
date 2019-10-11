from tornado import web
from .base import BaseHandler
from daos.userDao import UserDao
from models.user import User


class LoginHandler(BaseHandler):
    async def get(self):
        if self.current_user:
            self.redirect('/rss_reader')
        else:
            self.render('index.html')

    async def post(self):
        email = self.get_body_argument('email')
        input_password = self.get_body_argument('password').encode()
        user = User(email=email)
        user = await UserDao.get(user, get_by='email')
        if user:
            if await user.check_password(input_password):
                self.set_secure_cookie("user_id", str(user.id))
                self.redirect('/rss_reader')
            else:
                self.write('Wrong password')
        else:
            self.write('No such user!')

