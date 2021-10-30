from typing import Callable, Union, NewType

from django.conf import settings
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.errors import ConnectionFailure, OperationFailure

OptionalSession = NewType('OptionalSession', Union[Callable[[ClientSession], None], None])


class MongoDBClient:
    _instance: MongoClient = None

    def __new__(cls):
        if cls._instance is None:
            return MongoClient(settings.CUSTOM_MONGODB_URL)
        return cls._instance


class MongoAdapter:
    client = MongoDBClient()
    callable_fn: OptionalSession = None

    def __init__(self, database_name=settings.CUSTOM_MONGODB_DATABASE) -> None:
        self.database = self.client.get_database(database_name)

    def set_callable(self, callable_fn):
        self.callable_fn = callable_fn

    def get_collection(self, name):
        collection_list = list(self.database.list_collections())
        collection_exists = False
        for collection in collection_list:
            if collection['name'] == name:
                collection_exists = True
                break
        if collection_exists:
            return self.database.get_collection(name)
        else:
            return self.database.create_collection(name)


class DefaultMongoAdapter(MongoAdapter):
    def execute(self, **kwargs):
        self.callable_fn(**kwargs)


class TransactionEnabledMongoAdapter(DefaultMongoAdapter):

    def __init__(self, database_name=settings.CUSTOM_MONGODB_DATABASE) -> None:
        super().__init__(database_name)
        self.session = self.client.start_session()

    def execute(self, **kwargs):
        """
        Execute the transaction and commit the transaction. If error occurs, rollback the transaction
        """
        while True:
            try:
                with self.session.start_transaction():
                    result = self.callable_fn(self.session, **kwargs)
                    self.__commit_transaction()
                break
            except (ConnectionFailure, OperationFailure) as ex:
                print(
                    "Error during executing the query statements... Stopping transaction")
                if ex.has_error_label("TransientTransactionError"):
                    print("TransientTransactionError, retrying transaction ...")
                    continue
                else:
                    print(
                        "Error during executing the query statements... Stopping transaction")
                    raise
        return result

    def __commit_transaction(self):
        """
        Commit the transaction. If error occurs, rollback the transaction
        """
        while True:
            try:
                self.session.commit_transaction()
                break
            except (ConnectionFailure, OperationFailure) as ex:
                if ex.has_error_label("UnknownTransactionCommitResult"):
                    print(
                        "UnknownTransactionCommitResult, retrying commit operation ...")
                    continue
                else:
                    print("Error during commit ... Stopping transaction")
                    raise
