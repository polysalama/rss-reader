from tornado import web
from datetime import datetime
from daos.userDao import UserDao
from models.user import User
from aiosmtplib import SMTP
import bcrypt

class RegisterHandler(web.RequestHandler):

    async def get(self):
        await self.render('register.html')

    async def post(self):
        email = self.get_body_argument('email')
        password = self.get_body_argument('password').encode()
        user = User(email=email,
               created_at=datetime.now())
        if await UserDao.get(user, get_by='email'):
            self.write('exists')
            return
        reg_user = await UserDao.save(User(email=email, 
                                           password=await User.hash_password(password), 
                                           created_at=datetime.now()))
        print(reg_user.id, flush=True)
        print(reg_user.email, flush=True)
        smtp_client = SMTP(hostname=self.settings['smpt_host'], 
                           port=self.settings['smpt_port'],
                           username=self.settings['smpt_user'] if self.settings['smpt_user'] else None,
                           password=self.settings['smpt_password'] if self.settings['smpt_password'] else None)                 
        await reg_user.send_email(smtp_client, 'follow link')
        self.redirect('/register_ok')

class RegisterSuccessHandler(web.RequestHandler):

    async def get(self):
        try:
            if self.request.headers['Referer'].split('/')[-1] == 'register':
                await self.render('register_ok.html')
            else:
                self.redirect('/')
        except KeyError:
            self.redirect('/')

