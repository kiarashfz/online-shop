from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.apis import OrderViewSet, OrderItemViewSet, OrderItemOfProduct
from orders.views import NotLoginHandler

router = DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'order_items', OrderItemViewSet)

app_name = 'orders'
urlpatterns = [
    path('', include(router.urls)),
    path('order_item_of_product', OrderItemOfProduct.as_view(), name='order_item_of_product'),
    path('not_login_handler', NotLoginHandler.as_view(), name='not_login_handler'),
]
