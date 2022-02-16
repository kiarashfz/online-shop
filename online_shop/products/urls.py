from django.urls import path

from products.views import ProductListView

urlpatterns = [
    path('products_list/', ProductListView.as_view(), name='products_list'),
]