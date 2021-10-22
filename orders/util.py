import json

from bson.json_util import dumps
from uuid import uuid4
from bson import ObjectId

from .custom_exceptions import RecordNotFound
from .models import Product, Order
from shared.database import OrderCollection as OrderDB, ProductCollection as ProductDB

orders_collection = OrderDB()
products_collection = ProductDB()


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


def save_order(products: list[Product]) -> dict:
    """
    Saves order in mongodb
    :param products: List of products added for this orders
    :return: Dictionary of saved result
    """
    product_ids = []
    total_price = 0.0
    for order_product in products:
        product_id = _save_product(order_product)
        total_price += float(order_product.get('price') * order_product.get('quantity'))
        product_ids.append(product_id)
    order_id = uuid4().__str__()
    order = Order(order_id=order_id, total_price=total_price, products=product_ids)
    saved_order = orders_collection.insert_one(order)
    return {
        "order_id": order_id,
        "mongodb_id": json.loads(dumps(saved_order.inserted_id))
    }


def _save_product(product: Product) -> ObjectId:
    """
    Save a product to mongodb
    :param product: Product to be saved in mongodb
    :return: mongodb id
    """
    saved_product = products_collection.insert_one(product)
    return saved_product.inserted_id


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
