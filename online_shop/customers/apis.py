import logging

from rest_framework import generics, authentication, renderers
from rest_framework import permissions

from core.models import User
from customers.models import Customer, Address
from customers.permissions import IsSuperUserPermission, IsOwnerPermission, IsAddressOwnerPermission
from customers.serializers import CustomerSerializer, UserSerializer, AddressSerializer


class UserCreateApiView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CustomerCreateApiView(generics.CreateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class UserListApiView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsSuperUserPermission]
    authentication_classes = [authentication.BasicAuthentication]


class UserDetailApiView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerPermission]
    authentication_classes = [authentication.BasicAuthentication]


class AddressListApiView(generics.ListAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.BasicAuthentication]
    renderer_classes = [
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        renderers.AdminRenderer,
        renderers.TemplateHTMLRenderer,
    ]

    def get_queryset(self):
        return Address.objects.filter(customer__user=self.request.user)


class AddressDetailApiView(generics.RetrieveAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [IsAddressOwnerPermission]
    authentication_classes = [authentication.BasicAuthentication]

    def get_queryset(self):
        # logger = logging.getLogger('project.developers')
        logger = logging.getLogger('project')
        logger.error("error")
        return super().get_queryset()

    # def get_queryset(self):
    #     return Address.objects.filter(customer__user=self.request.user)


class AddressDeleteApiView(generics.DestroyAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(customer__user=self.request.user)


class AddressCreateApiView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(customer__user=self.request.user)

    def perform_create(self, serializer):
        customer = Customer.objects.get(user=self.request.user)
        serializer.save(customer=customer)


class UserUpdateApiView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.id)


class CustomerUpdateApiView(generics.UpdateAPIView):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)
