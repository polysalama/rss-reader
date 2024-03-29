from .dao import Dao
from models.users_rss import UsersRss
from models.rss import Rss


class UsersRssDao(Dao):

    @staticmethod
    async def save(user, rss):
        # Save users rss

        sql = 'INSERT INTO users_rss (user_id, rss_id) VALUES (%s, %s);'
        await UsersRssDao.DB.execute(sql, [user.id, rss.id])

    @staticmethod
    async def get_all_user_rss(user):
        # Get all the users rss

        sql = 'SELECT rss.rss_id, rss.title, rss.link FROM users_rss INNER JOIN rss ON  rss.rss_id = users_rss.rss_id WHERE users_rss.user_id=%s'
        cursor = await UsersRssDao.DB.execute(sql, [user.id])
        results = cursor.fetchall()
        return list(map(lambda item: Rss(item[0], item[1], item[2]), results))

    @staticmethod
    async def rss_set_to_user(user, rss):
        # Check if rrs is associated with the user

        sql = 'SELECT EXISTS (SELECT rss.rss_id, rss.title, rss.link FROM users_rss INNER JOIN rss ON  rss.rss_id = users_rss.rss_id WHERE users_rss.user_id=%s AND users_rss.rss_id=%s)'
        cursor = await UsersRssDao.DB.execute(sql, [user.id, rss.id])
        result = cursor.fetchone()
        return result[0]
