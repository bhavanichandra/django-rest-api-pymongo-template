import json

from bson.json_util import dumps
from uuid import uuid4
from pymongo.client_session import ClientSession

from .models import Product, Order
from shared.database_transactions import MongoAdapter
from .custom_exceptions import RecordNotFound

mongo_adapter = MongoAdapter()
products_collection = mongo_adapter.get_collection('products')
orders_collection = mongo_adapter.get_collection('orders')


# No Transaction used for get_all_orders
def get_all_orders(expand_products: bool = False) -> str:
    """ Get all orders from database
    Arguments:
       :param expand_products: To expand all products
       :type  expand_products: boolean
    """
    if expand_products:
        aggregate = [
            {"$lookup": {"from": "products", "localField": "products", "foreignField": "_id", "as": "products"}}
        ]
        orders_list = orders_collection.aggregate(aggregate)
    else:
        orders_list = list(orders_collection.find())
    return json.loads(dumps(orders_list))


def save_order(session: ClientSession, products: list[Product]) -> dict:
    """
    Saves order in mongodb
    :param products: List of products added for this orders
    :param session: Database Session to execute
    :return: Dictionary of saved result
    """
    product_ids = []
    total_price = 0.0
    for order_product in products:
        saved_product = products_collection.insert_one(order_product, session=session)
        total_price += float(order_product.get('price') * order_product.get('quantity'))
        product_ids.append(saved_product.inserted_id)
    order_id = uuid4().__str__()
    order = Order(order_id=order_id, total_price=total_price, products=product_ids)
    saved_order = orders_collection.insert_one(order, session=session)
    return {
        "order_id": order_id,
        "mongodb_id": json.loads(dumps(saved_order.inserted_id))
    }


def get_products_by_name(name: str) -> list[Product]:
    """
    Get products by name
    :param name: Product Name
    :return: list of products
    """
    products_cursor = products_collection.find({"name": name})
    products = json.loads(dumps(products_cursor))
    if len(products) != 0:
        return products
    else:
        print('Error')
        raise RecordNotFound()
