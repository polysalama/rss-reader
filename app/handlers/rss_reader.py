from tornado import web
from tornado.httpclient import AsyncHTTPClient
from .base import BaseHandler
from daos.rssDao import RssDao
from models.rss import Rss, RssParser
from daos.usersRssDao import UsersRssDao
from models.users_rss import UsersRss
from models.user import User
from tornado.template import Template
import json

class RssHandler(BaseHandler):
    @web.authenticated
    async def get(self):
        user_id = self.get_current_user().decode()
        cache = await self.application.redis.get(user_id)
        if cache:
            self.render('rss_reader.html', rss_feed=json.loads(cache))
        else:
            all_rss = await UsersRssDao.get_all_user_rss(User(id=user_id))
            rss_content = await RssParser.fetch_all_rss_content(all_rss)
            rss_content = await RssParser.parse_list_of_rss_xmls(rss_content, all_rss)
            await self.application.redis.set(user_id, json.dumps(rss_content))
            await self.application.redis.expire(user_id, 5)
            await self.render('rss_reader.html', rss_feed=rss_content)

    @web.authenticated
    async def post(self):
        user_id = self.get_current_user().decode()
        user = User(id=user_id)
        rss_link = self.get_body_argument('rss_link')
        rss = Rss(link=rss_link)
        rss = await RssDao.get(rss)
        if not rss:
            rss = Rss(link=rss_link)
            http_client = AsyncHTTPClient()
            try:
                response = await http_client.fetch(rss_link)
            except Exception as e:
                self.write('network error')
                return
            tree = await RssParser.xml_to_tree(response.body)
            if tree and await RssParser.rss_is_valid(tree):
                rss.title = await RssParser.rss_feed_title(tree)
                rss = await RssDao.save(rss) 
            else:
                self.write('not valid rss')
                return
        print(await UsersRssDao.rss_set_to_user(user, rss), flush=True)
        if not await UsersRssDao.rss_set_to_user(user, rss):
            await UsersRssDao.save(user, rss)
            await self.application.redis.delete(user_id)
        self.redirect('/rss_reader')
