from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .custom_exceptions import RecordNotFound
from .models import Product

from . import util

from shared import wrapper, helper


class OrdersView(APIView):
    def get(self, request):
        try:
            # order = Order()
            expand_products = False
            query_param_expand = helper.get_query_param_value(request.query_params, 'expand_products')
            print(query_param_expand)
            if query_param_expand is not None:
                expand_products = True if query_param_expand[0] == 'true' else False
            order_list = util.get_all_orders(expand_products)
            data = wrapper.SuccessWrapper(order_list)
            return Response(data=data.__dict__, status=HTTP_200_OK)
        except Exception as e:
            data = wrapper.ErrorWrapper(e.__str__())
            return Response(data=data.__dict__, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            print(f"request data: {request.data}")
            selected_products: list[Product] = list(request.data)
            products = [Product(price=product['price'], name=product['name'], quantity=product['quantity'])
                        for product in selected_products]
            saved_order = util.save_order(products)
            response_data = wrapper.SuccessWrapper(saved_order)
            return Response(data=response_data.__dict__, status=HTTP_201_CREATED)
        except Exception as e:
            data = wrapper.ErrorWrapper(e.__str__())
            return Response(data=data.__dict__, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ProductView(APIView):
    def get(self, request, name):
        try:
            print(f"Product Name: {name}")
            products_by_name = util.get_products_by_name(name)
            data = wrapper.SuccessWrapper(products_by_name)
            return Response(data=data.__dict__, status=HTTP_200_OK)
        except RecordNotFound as rfe:
            data = wrapper.ErrorWrapper(rfe.__str__())
            return Response(data=data.__dict__, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            data = wrapper.ErrorWrapper(e.__str__())
            return Response(data=data.__dict__, status=HTTP_500_INTERNAL_SERVER_ERROR)
