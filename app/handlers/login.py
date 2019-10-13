from tornado import web
from .base import BaseHandler
from daos.userDao import UserDao
from models.user import User


class LoginHandler(BaseHandler):
    async def get(self):
        if self.current_user:
            self.redirect('/rss_reader')
        else:
            await self.render('login.html', status='')

    async def post(self):
        email = self.get_body_argument('email')
        input_password = self.get_body_argument('password').encode()
        user = User(email=email)
        user = await UserDao.get(user, get_by='email')
        if not user or not await user.check_password(input_password):
            await self.render('login.html', status='bad_login')
        else:
            self.set_secure_cookie("user_id", str(user.id))
            self.redirect('/rss_reader')

class LogoutHandler(BaseHandler):
    
    @web.authenticated
    async def get(self):
        user_id = self.get_current_user().decode()
        self.clear_cookie('user_id', path='/')
        self.redirect('/')

class RedirectHandler(BaseHandler):
    
    async def get(self):
        self.redirect('/login')

  

