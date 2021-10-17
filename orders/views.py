from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED
from rest_framework.views import APIView

from .database_legacy import Order, Product


# Create your views here.


class OrdersView(APIView):
    def get(self, request):
        try:
            order = Order()
            order_list = order.get_all_orders()
            data = {
                'success': True,
                'result': order_list
            }
            return Response(data=data, status=HTTP_200_OK)
        except Exception as e:
            e.with_traceback()
            print(e)
            data = {
                'success': False,
                'result': None
            }
            return Response(data=data, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            selected_products = list(request.data)
            products = [Product(product['price'], product['quantity'], product['name']) for product in selected_products]
            product_ids = []
            for product in products:
                saved_product_id = product.save()
                product_ids.append(saved_product_id['_id'])
            order = Order(products=product_ids)
            saved_order = order.save()
            response_data = {
                'success': True,
                'result': saved_order
            }
            return Response(data=response_data, status=HTTP_201_CREATED)
        except Exception as e:
            e.with_traceback()
            data = {
                'success': False,
                'result': None,
                'error_message': e
            }
            return Response(data=data, status=HTTP_500_INTERNAL_SERVER_ERROR)
