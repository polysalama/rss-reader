from abc import ABCMeta, abstractmethod

class Dao(metaclass=ABCMeta):

    DB = None

    @staticmethod
    @abstractmethod
    async def get():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def update():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def delete():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def save():
        raise NotImplementedError