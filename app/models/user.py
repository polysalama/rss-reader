from tornado.ioloop import IOLoop
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import bcrypt

class User(): 

    executor = None
    
    def __init__(self, id=None, email=None, password=None, created_at=None):
            self.id = id
            self.email=email
            self.password=password
            self.created_at=created_at
    
    async def check_password(self, input_password):
        # Checks hashed and input password

        return await IOLoop.current().run_in_executor(User.executor, bcrypt.checkpw, input_password, self.password)

    async def send_email(self, smtp_client, email_body):
        # Sends conformation mail to user

        message = MIMEMultipart('alternative')
        message['From'] = 'root@localhost'
        message['To'] = self.email
        message['Subject'] = 'Follow link'
        message.attach(MIMEText(email_body, 'plain'))
        await smtp_client.connect()
        await smtp_client.send_message(message)
        await smtp_client.quit()

    @staticmethod
    async def hash_password(password):
        return await IOLoop.current().run_in_executor(User.executor, 
                                                        bcrypt.hashpw, 
                                                        password, 
                                                        bcrypt.gensalt())
