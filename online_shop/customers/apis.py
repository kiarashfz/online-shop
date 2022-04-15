import logging

from rest_framework import generics, authentication, renderers
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User
from customers.models import Customer, Address
from customers.permissions import IsSuperUserPermission, IsOwnerPermission, IsAddressOwnerPermission
from customers.serializers import CustomerSerializer, UserSerializer, AddressSerializer, CommentSerializer

import random
from kavenegar import *

from products.models import Comment


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


class AddressUpdateApiView(generics.UpdateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

    def get_queryset(self):
        return Address.objects.filter(customer__user=self.request.user)


class ConfirmCode(APIView):
    def get(self, request):
        confirm_code = random.randint(1000, 9999)
        phone = request.GET.get('phone', None)
        try:
            api = KavenegarAPI(
                '63692F4778315056363552346E79796C55624C765973447649314859516156705A706557763430634D48513D')
            params = {
                'sender': '10008663',
                'receptor': f'{phone}',
                'message': f'Hi !\nWelcome to Web Mall!\n\nYour confirm code: {confirm_code}',
            }
            print(confirm_code)
            # response = api.sms_send(params)
        except APIException as e:
            print(e)
            return Response(status=400)
        except HTTPException as e:
            print(e)
            return Response(status=400)
        request.session['confirm_code'] = confirm_code
        return Response(status=200)


class CommentUpdateApiView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
