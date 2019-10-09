from tornado import web
from datetime import datetime
from tornado.ioloop import IOLoop
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
import bcrypt

class RegisterHandler(web.RequestHandler):

    async def get(self):
        await self.render('register.html')

    async def post(self):
        sql = 'INSERT INTO users (email, password, created_at) VALUES (%s, %s, %s);'
        email = self.get_body_argument('email')
        password = await IOLoop.current().run_in_executor(None, 
                lambda: bcrypt.hashpw(self.get_body_argument('password').encode(), 
                                      bcrypt.gensalt()))
        values = [email,
                  password,
                  datetime.now()]
        await self.application.db.execute(sql, values)
        message = MIMEMultipart('alternative')
        message['From'] = 'root@localhost'
        message['To'] = 'somebody@example.com'
        message['Subject'] = 'Follow link'
        message.attach(MIMEText('hello', 'plain'))
        await aiosmtplib.send(message, 
                              sender='bla@bla.com', 
                              recipients='bla@neki.com', 
                              hostname=self.settings['smpt_host'], 
                              port=self.settings['smpt_port'],
                              username=self.settings['smpt_user'] if self.settings['smpt_user'] else None,
                              password=self.settings['smpt_password'] if self.settings['smpt_password'] else None
                              )
        self.render('register_ok.html')

