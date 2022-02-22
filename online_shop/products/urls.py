from django.urls import path

from products.views import ProductListView, ProductDetailView
from .aips import ProductListApiView, ProductDetailApiView

app_name = 'products'
urlpatterns = [
    path('products_list/', ProductListView.as_view(), name='products_list'),
    path('product_detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    # path('products_list_api/', product_list_api, name='products_list_api'),
    path('products_list_api/', ProductListApiView.as_view(), name='products_list_api'),
    path('products_detail_api/<int:pk>', ProductDetailApiView.as_view(), name='products_detail_api'),
    # path('products_tamplate/', ProductTemplateView.as_view(), name='products_template'),
]
