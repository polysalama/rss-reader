from tornado import web
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib

class MainHandler(web.RequestHandler):
    async def get(self):
        self.render('index.html')
        message = MIMEMultipart('alternative')
        message['From'] = 'root@localhost'
        message['To'] = 'somebody@example.com'
        message['Subject'] = 'Hello World'
        message.attach(MIMEText('hello', 'plain'))
        msg = await aiosmtplib.send(message, 
                                    sender='bla@bla.com', 
                                    recipients='bla@neki.com', 
                                    hostname=self.settings['smpt_host'], 
                                    port=self.settings['smpt_port'],
                                    username=self.settings['smpt_user'] if self.settings['smpt_user'] else None,
                                    password=self.settings['smpt_password'] if self.settings['smpt_password'] else None
                                    )
