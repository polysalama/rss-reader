from tornado.httpclient import AsyncHTTPClient
from tornado.gen import multi
from xmlschema import XMLSchema
from tornado.ioloop import IOLoop
import defusedxml.ElementTree as ET

class Rss(): 
    
    def __init__(self, id=None, title=None, link=None):
            self.id = id
            self.title=title
            self.link=link

class RssParser:

    xml_schema = XMLSchema('rss_schema.xsd')

    @staticmethod
    async def rss_is_valid(tree):
        # Validate xml with rss schema

        return await IOLoop.current().run_in_executor(None, lambda: RssParser.xml_schema.is_valid(tree))

    @staticmethod
    async def xml_to_tree(xml):
        try:
            return await IOLoop.current().run_in_executor(None, lambda: ET.fromstring(xml))
        except ET.ParseError:
            return None

    @staticmethod
    async def rss_feed_title(tree):
        return await IOLoop.current().run_in_executor(None, lambda: tree.find('channel').find('title').text)

    @staticmethod
    async def fetch_all_rss_content(rss_list):
        # Fetches xmls for all rss feeds and returns them in a list

        http_client = AsyncHTTPClient()
        responses = await multi ([http_client.fetch(rss.link) for rss in rss_list])
        return [response.body for response in responses]

    @staticmethod
    async def parse_list_of_rss_xmls(rss_list, all_rss):
        # Parse all retrieved xmls and return them in list

        return await multi ([RssParser.parse_rss_content_to_list(rss_xml, rss.title) for rss_xml, rss in zip(rss_list, all_rss)])

    @staticmethod
    async def parse_rss_content_to_list(rss_xml, rss_title):
        # Parse and store xml content to a dictionary

        return_list = []
        tree = await RssParser.xml_to_tree(rss_xml)
        channel = await IOLoop.current().run_in_executor(None, lambda: tree.find('channel'))
        children = list(channel)
        if children:
            items = filter(lambda i: i.tag == 'item', children)
            for item in items:
                item_children = list(item)
                return_list.append(dict(map(lambda x: (x.tag, x.text), item_children)))
        return {'rss_title': rss_title, 'feed': return_list}
