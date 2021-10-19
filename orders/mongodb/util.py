import json

from bson.json_util import dumps

from .database import Order, Product

orders_collection = Order()
products_collection = Product()


def get_all_orders(expand_products=False):
    """ Get all orders from database

    Arguments:
        expand_products -- TO expand all products
    """
    if expand_products:
        aggregate = [
            {"$lookup": {"from": "products", "localField": "products", "foreignField": "_id", "as": "products"}}
        ]
        orders_list = orders_collection.aggregate(aggregate)
    else:
        orders_list = list(orders_collection.find())
    return json.loads(dumps(orders_list))
