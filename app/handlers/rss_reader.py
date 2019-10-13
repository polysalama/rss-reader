from tornado import web
from tornado.httpclient import AsyncHTTPClient
from .base import BaseHandler
from daos.rssDao import RssDao
from models.rss import Rss, RssParser
from daos.usersRssDao import UsersRssDao
from models.users_rss import UsersRss
from models.user import User
from tornado.template import Template

class RssHandler(BaseHandler):
    @web.authenticated
    async def get(self):
        all_rss = await UsersRssDao.get_all_user_rss(User(id=self.get_current_user().decode()))
        rss_content = await RssParser.fetch_all_rss_content(all_rss)
        rss_content = await RssParser.parse_list_of_rss_xmls(rss_content)
        self.render('rss_reader.html', rss_feed=list(zip(all_rss, rss_content)))

    @web.authenticated
    async def post(self):
        rss_link = self.get_body_argument('rss_link')
        rss = Rss(link=rss_link)
        return_rss = await RssDao.get(rss)
        if not return_rss:
            http_client = AsyncHTTPClient()
            try:
                response = await http_client.fetch(rss_link)
            except Exception as e:
                self.render('rss_reader.html', rss_feed=list(zip(all_rss, rss_content)))
                return
            tree = await RssParser.xml_to_tree(response.body)
            if tree and await RssParser.rss_is_valid(tree):
                rss.title = await RssParser.rss_feed_title(tree)
                rss = await RssDao.save(rss) 
            else:
                self.write('not valid rss')
                return
        await UsersRssDao.save(User(id=self.get_current_user().decode()), rss)
        self.redirect('/rss_reader')
