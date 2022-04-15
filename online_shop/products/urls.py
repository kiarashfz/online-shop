from django.urls import path

from products.views import ProductListView, ProductDetailView, CategoryDetailView
from .apis import ProductListApiView, ProductDetailApiView, CategoryProductsListApiView, CommentCreateApiView

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(), name='products_list'),
    path('product_detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
    # path('products_list_api/', product_list_api, name='products_list_api'),
    path('products_list_api/', ProductListApiView.as_view(), name='products_list_api'),
    path('comment_create_api/', CommentCreateApiView.as_view(), name='comment_create_api'),
    path('products_detail_api/<int:pk>', ProductDetailApiView.as_view(), name='products_detail_api'),
    path('category_detail/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('category_products_list_api/<int:category_id>', CategoryProductsListApiView.as_view(), name='category_products_list_api'),
    # path('products_tamplate/', ProductTemplateView.as_view(), name='products_template'),
]
