from rest_framework import generics

from core.models import User
from customers.models import Customer
from customers.serializers import CustomerSerializer, UserSerializer


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CustomerCreateApiView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
