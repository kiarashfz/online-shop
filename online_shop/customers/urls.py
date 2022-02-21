from django.urls import path

from customers.apis import CustomerCreateApiView

urlpatterns = [
    path('customer_create_api/', CustomerCreateApiView.as_view(), name='customer_create_api'),
]
