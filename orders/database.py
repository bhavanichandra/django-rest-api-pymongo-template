from pymongo import MongoClient
from uuid import uuid4
from bson import ObjectId
from bson.json_util import dumps
import json

from .custom_exceptions import DatabaseInitException

client = MongoClient('mongodb+srv://api_user:Th3q02nCvzUF4lUI@cluster0.yerkz.mongodb.net')
orders_tracker = client['orders_tracker']
collections = list(orders_tracker.list_collections())


def does_collection_exists(collection_name):
    """ Checks if collection exists on mongodb

     Attributes:
         collection_name -- Name of the collection to check
     """
    for collection in collections:
        if collection['name'] == collection_name:
            return True
        else:
            return False


class Order:
    orders = None
    collection_name = 'orders'

    def __init__(self, products=None):
        self.init()
        if products is None:
            products = []
        self.order_id = uuid4().__str__()
        self.total_price = 0.00
        self.products = products

    def init(self):
        if does_collection_exists(self.collection_name):
            self.orders = orders_tracker.create_collection(self.collection_name)
        else:
            self.orders = orders_tracker.get_collection(self.collection_name)

    def calculate_total_price(self):
        self.total_price = sum([product.get('price') for product in self.products])

    def get_all_orders(self):
        aggregate = [
            {"$lookup": {"from": "products", "localField": "products", "foreignField": "_id", "as": "products"}}
        ]
        return json.loads(dumps(self.orders.aggregate(aggregate)))

    def get_order_by_id(self, pk):
        mongo_id = ObjectId(pk)
        return json.loads(dumps(self.orders.find_one({'_id': mongo_id})))

    def save(self):
        if self.orders is None:
            raise DatabaseInitException(f"{self.collection_name} collection is not iniz̧tialized")
        order = {
            'products': self.products,
            'total_price': self.calculate_total_price()
        }
        print(order)
        inserted_order = self.orders.insert_one(order)
        order['_id'] = inserted_order.__dict__['_id']
        print(order)
        return order


class Product:
    products = None
    collection_name = 'products'

    def __init__(self, price, quantity, name):
        self.init()
        self.price = price
        self.quantity = quantity
        self.name = name

    def init(self):
        if not does_collection_exists(self.collection_name):
            self.products = orders_tracker.create_collection(self.collection_name)
        else:
            self.products = orders_tracker.get_collection(self.collection_name)

    def save(self):
        if self.products is None:
            raise DatabaseInitException(f"{self.collection_name} collection is not initialized")
        product = {
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price
        }
        print(product)
        inserted_product = self.products.insert_one(product)
        product['_id'] = inserted_product.inserted_id
        return json.loads(dumps(product))
