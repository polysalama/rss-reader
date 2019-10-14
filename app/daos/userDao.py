from .dao import Dao
from datetime import datetime
from psycopg2.errors import UniqueViolation
from psycopg2.sql import Identifier, SQL
from models.user import User
import bcrypt

class UserDao(Dao):

    @staticmethod
    async def save(user):
        # Save user and return it with new id

        sql = 'INSERT INTO users (email, password, created_at) VALUES (%s, %s, %s) RETURNING user_id;'
        cursor = await UserDao.DB.execute(sql, [user.email, 
                                                user.password, 
                                                user.created_at])
        result = cursor.fetchone()                                     
        return User(id=result[0], 
                    email=user.email, 
                    password=None,
                    created_at=user.created_at)

    @staticmethod
    async def get(user, get_by='user_id'):
        # Retrieve user by id or email

        sql = 'SELECT * FROM users WHERE {}=%s'
        values = [user.id if get_by == 'user_id' else user.email]
        cursor = await UserDao.DB.execute(SQL(sql).format(Identifier(get_by)), 
                                          values)      
        result = cursor.fetchone()                                
        if result:
            return User(id=result[0], 
                        email=result[1], 
                        password=result[2].tobytes(),
                        created_at=result[3])
        else: 
            return None

    @staticmethod
    async def delete():
        pass 
        
    @staticmethod
    async def update():
        pass
