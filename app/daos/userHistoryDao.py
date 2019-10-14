from .dao import Dao
from models.user import User
from models.user_history import UserHistory

class UserHistoryDao(Dao):

    @staticmethod
    async def save(user_history):
        sql = 'INSERT INTO user_history (login_date, user_id) VALUES (%s, %s);'
        cursor = await UserHistoryDao.DB.execute(sql, [user_history.date, 
                                                       user_history.user_id])
    @staticmethod
    async def get(user):
        sql = 'SELECT login_date FROM user_history WHERE user_id=%s'
        cursor = await UserHistoryDao.DB.execute(sql, [user.id])      
        result = cursor.fetchall()                                
        if result:
            return UserHistory(date=list(map(lambda x: x[0].strftime('%d/%m/%Y, %H:%M:%S'), result)), 
                               user_id=user.id)
        else: 
            return None