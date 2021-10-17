from typing import TypeVar, Generic

from django.conf import settings
from pymongo import MongoClient

T = TypeVar('T')


class MongoDBClient(object):
    _instance = None
    _connection_str = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._connection_str = settings.CUSTOM_MONGODB_URL

    def __db(self, database_name):
        client = MongoClient(self._connection_str)
        database = client[database_name]
        return database


class Collection(Generic[T]):
    def __init__(self, collection_name) -> None:
        self.collection_name = collection_name
