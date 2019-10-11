from .dao import Dao
from datetime import datetime
from psycopg2.errors import UniqueViolation
import bcrypt

class RssDao(Dao):

    @staticmethod
    async def save(rss):
        sql = 'INSERT INTO rss (title, link) VALUES (%s, %s); RETURNING rss_id'
        try:
            await RssDao.DB.execute(sql, [rss.title, 
                                           rss.link])
        except UniqueViolation as e:
            return e

    @staticmethod
    async def get(rss):
        sql = 'SELECT FROM rss '

    @staticmethod
    async def exists(rss):
        sql = 'SELECT EXISTS (SELECT 1 FROM rss WHERE link=%s)'
        cursor = await RssDao.DB.execute(sql, [rss.link])
        return cursor.fetchone()[0]

    @staticmethod
    async def delete():
        pass 
        
    @staticmethod
    async def update():
        pass 

