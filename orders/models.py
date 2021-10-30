from bson import ObjectId
from typing_extensions import TypedDict
# Create your models here.


Product = TypedDict('Product', {'name': str, 'price': float, 'quantity': int})
Order = TypedDict('Order', {'order_id': str, 'total_price': float, 'products': list[ObjectId]})
