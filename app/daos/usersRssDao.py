from .dao import Dao
from models.users_rss import UsersRss
from models.rss import Rss


class UsersRssDao(Dao):

    @staticmethod
    async def save(user, rss):
        sql = 'INSERT INTO users_rss (user_id, rss_id) VALUES (%s, %s);'
        await UsersRssDao.DB.execute(sql, [user.id, rss.id])

    @staticmethod
    async def get_all_user_rss(user):
        sql = 'SELECT rss.rss_id, rss.title, rss.link FROM users_rss INNER JOIN rss ON  rss.rss_id = users_rss.rss_id WHERE users_rss.user_id=%s'
        cursor = await UsersRssDao.DB.execute(sql, [user.id])
        results = cursor.fetchall()
        return list(map(lambda item: Rss(item[0], item[1], item[2]), results))