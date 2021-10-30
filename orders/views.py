from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from .custom_exceptions import RecordNotFound
from shared.database_transactions import TransactionEnabledMongoAdapter
from .models import Product

from . import repository

from shared import wrapper, helper

mongo_with_transactions = TransactionEnabledMongoAdapter()


class OrdersView(APIView):
    def get(self, request):
        """
        Get all orders
        :param request: Http Request
        :return: List of Orders
        """
        try:
            expand_products = False
            query_param_expand = helper.get_query_param_value(request.query_params, 'expand_products')
            print(query_param_expand)
            if query_param_expand is not None:
                expand_products = True if query_param_expand[0] == 'true' else False
            order_list = repository.get_all_orders(expand_products)
            data = wrapper.SuccessWrapper(order_list)
            return Response(data=data.__dict__, status=HTTP_200_OK)
        except Exception as e:
            data = wrapper.ErrorWrapper(e.__str__())
            return Response(data=data.__dict__, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        Create a new order
        :param request: Http Request
        :return: New Order
        """
        try:
            print(f"request data: {request.data}")
            selected_products: list[Product] = list(request.data)
            products = [Product(price=product['price'], name=product['name'], quantity=product['quantity'])
                        for product in selected_products]
            mongo_with_transactions.set_callable(callable_fn=repository.save_order)
            saved_order = mongo_with_transactions.execute(products=products)
            response_data = wrapper.SuccessWrapper(saved_order)
            return Response(data=response_data.__dict__, status=HTTP_201_CREATED)
        except Exception as e:
            data = wrapper.ErrorWrapper(e.__str__())
            return Response(data=data.__dict__, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ProductView(APIView):
    def get(self, request, name):
        """
        Get a product by name
        :param request: Http Request
        :param name: Name of the product
        :return: Product
        """
        try:
            print(f"Product Name: {name}")
            products_by_name = repository.get_products_by_name(name)
            data = wrapper.SuccessWrapper(products_by_name)
            return Response(data=data.__dict__, status=HTTP_200_OK)
        except RecordNotFound as rfe:
            data = wrapper.ErrorWrapper(rfe.__str__())
            return Response(data=data.__dict__, status=HTTP_404_NOT_FOUND)
        except Exception as e:
            data = wrapper.ErrorWrapper(e.__str__())
            return Response(data=data.__dict__, status=HTTP_500_INTERNAL_SERVER_ERROR)
