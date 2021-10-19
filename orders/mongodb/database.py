from django.conf import settings
from pymongo import MongoClient


class MongoDBClient(object):
    _instance = None
    _connection_str = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._connection_str = settings.CUSTOM_MONGODB_URL
        return cls._instance

    def __db__(self, database_name):
        client = MongoClient(self._connection_str)
        database = client[database_name]
        return database


class Collection:
    @staticmethod
    def get_collection(name: str, dbname: str):
        client = MongoDBClient()
        database = client.__db__(dbname)
        collection_list = list(database.list_collections())
        does_collection_exists = False
        for collection in collection_list:
            if collection['name'] == name:
                does_collection_exists = True
                break
        if does_collection_exists:
            return database.get_collection(name)
        else:
            return database.create_collection(name)


class Order:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            return Collection.get_collection('orders', settings.CUSTOM_MONGODB_DATABASE)
        return cls._instance


class Product:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            return Collection.get_collection('orders', settings.CUSTOM_MONGODB_DATABASE)
        return cls._instance
