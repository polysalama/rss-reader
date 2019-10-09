from tornado import web
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .base import BaseHandler
import aiosmtplib

class RssHandler(BaseHandler):
    @web.authenticated
    async def get(self):
        self.render('rss_reader.html')

