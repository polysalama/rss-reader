from .dao import Dao
from datetime import datetime
from psycopg2.errors import UniqueViolation
from models.rss import Rss

class RssDao(Dao):

    @staticmethod
    async def save(rss):
        sql = 'INSERT INTO rss (title, link) VALUES (%s, %s) RETURNING rss_id'
        cursor = await RssDao.DB.execute(sql, [rss.title, 
                                               rss.link])
        result = cursor.fetchone()
        return Rss(id=result[0],
                   title=rss.title,
                   link=rss.link)

    @staticmethod
    async def get(rss):
        sql = 'SELECT * FROM rss WHERE link=%s'
        cursor = await RssDao.DB.execute(sql, [rss.link])
        result = cursor.fetchone()
        if result:
            return Rss(id=result[0],
                       title=result[1],
                       link=result[2])
        else:
            return None

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

