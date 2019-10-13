from tornado import web
from datetime import datetime
from daos.userDao import UserDao
from models.user import User
from aiosmtplib import SMTP
import bcrypt

class RegisterHandler(web.RequestHandler):

    async def get(self):
        await self.render('login.html', status='')

    async def post(self):
        email = self.get_body_argument('email')
        password = self.get_body_argument('password').encode()
        user = User(email=email,
               created_at=datetime.now())
        if await UserDao.get(user, get_by='email') is not None:
            await self.render('login.html', status='bad_register')
            return
        reg_user = await UserDao.save(User(email=email, 
                                           password=await User.hash_password(password), 
                                           created_at=datetime.now()))
        smtp_client = SMTP(hostname=self.settings['smpt_host'], 
                           port=self.settings['smpt_port'],
                           username=self.settings['smpt_user'] if self.settings['smpt_user'] else None,
                           password=self.settings['smpt_password'] if self.settings['smpt_password'] else None)                 
        await reg_user.send_email(smtp_client, f'Go to http://{self.settings["hostname"]}/login to login.')
        self.redirect('/register_ok')

class RegisterSuccessHandler(web.RequestHandler):

    async def get(self):
        try:
            ref = self.request.headers['Referer'].split('/')[-1]
            if ref == 'register' or ref == 'login' or ref == '':
                await self.render('register_ok.html')
            else:
                self.redirect('/')
        except KeyError:
            self.redirect('/')

