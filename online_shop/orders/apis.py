from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from rest_framework import generics, viewsets, renderers
from rest_framework.response import Response

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


class OrderItemOfProduct(generics.ListAPIView):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        if self.request.user.id:
            return OrderItem.objects.filter(customer__user=self.request.user)
        else:
            return []

    def get(self, request, *args, **kwargs):
        if self.request.user.id:
            serializer = OrderItemSerializer(self.get_queryset().get(product__id=request.GET['product_id']))
            return Response(serializer.data)
        else:
            response = HttpResponse('bad request!')
            response.status_code = 400
            return response
