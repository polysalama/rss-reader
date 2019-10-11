from tornado import web
from tornado.httpclient import AsyncHTTPClient
from .base import BaseHandler
from daos.rssDao import RssDao
from models.rss import Rss
from xmlschema import XMLSchema
from tornado.ioloop import IOLoop
import defusedxml.ElementTree as ET

class RssHandler(BaseHandler):
    @web.authenticated
    async def get(self):
        self.render('rss_reader.html')

    @web.authenticated
    async def post(self):
        rss_link = self.get_body_argument('rss_link')
        rss = Rss(link=rss_link)
        if await RssDao.exists(rss):
            self.write('exist')
        else:
            http_client = AsyncHTTPClient()
            try:
                response = await http_client.fetch(rss_link)
            except Exception as e:
                print("Error: %s" % e)
            else:
                tree = await RssParser.xml_to_tree(response.body)
                if await RssParser.rss_is_valid(tree):
                    rss.title = await RssParser.rss_feed_title(tree)
                    await RssDao.save(rss)
                    self.redirect('/rss_reader')
                else:
                    self.write('false rss')

class RssParser:

    xml_schema = XMLSchema('rss_schema.xsd')

    @staticmethod
    async def rss_is_valid(tree):
        return await IOLoop.current().run_in_executor(None, lambda: RssParser.xml_schema.is_valid(tree))

    @staticmethod
    async def xml_to_tree(xml):
        return await IOLoop.current().run_in_executor(None, lambda: ET.fromstring(xml))

    @staticmethod
    async def rss_feed_title(tree):
        return await IOLoop.current().run_in_executor(None, lambda: tree.find('channel').find('title').text)


    