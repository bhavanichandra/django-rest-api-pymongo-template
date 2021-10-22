from django.urls import path

from . import views

urlpatterns = [
    path('orders', views.OrdersView.as_view()),
    path('products/<str:name>', views.ProductView.as_view())
]
