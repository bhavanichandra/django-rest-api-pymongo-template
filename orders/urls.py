from django.urls import path

from . import views

urlpatterns = [
    path('orders', views.OrdersView.as_view())
]
