from django.contrib.auth.models import AnonymousUser
from django.contrib.humanize.templatetags.humanize import intcomma
from django.http import HttpResponse
from rest_framework import generics, viewsets, renderers
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from products.models import OffCode
from products.templatetags.product_extras import toman_format


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
            serializer = OrderItemSerializer(self.get_queryset().get(product__id=request.GET['product_id'], status=0))
            return Response(serializer.data)
        else:
            response = HttpResponse('bad request!')
            response.status_code = 400
            return response


class AfterOffCodeApiView(APIView):
    def post(self, request):
        after_off_code = intcomma(toman_format(int(Order.after_off_code_price(OffCode.objects.get(id=request.POST['off_code_id']), int(request.POST['total_price'])))))
        return Response(after_off_code, status=200)
