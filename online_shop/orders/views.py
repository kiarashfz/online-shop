from django.http import HttpResponse, QueryDict
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView

from orders.models import OrderItem
from products.models import Product


class NotLoginHandler(View):
    def post(self, request):
        if request.session.get('order_items', None):
            request.session['order_items'].update({request.POST['product_id']: 1})
            request.session['order_items'] = request.session['order_items']
        else:
            request.session['order_items'] = {request.POST['product_id']: 1}
        return HttpResponse('ok')

    def patch(self, request):
        data = QueryDict(request.body)
        request.session['order_items'][data['product_id']] = int(data['count'])
        request.session['order_items'] = request.session['order_items']
        return HttpResponse('ok')

    def delete(self, request):
        data = QueryDict(request.body)
        del request.session['order_items'][data['product_id']]
        request.session['order_items'] = request.session['order_items']
        return HttpResponse('ok')


class OrderItemListView(ListView):
    model = OrderItem
    queryset = OrderItem.objects.all()

    def get_queryset(self):
        if self.request.user.id:
            return OrderItem.objects.filter(customer__user=self.request.user)
        else:
            result = []
            order_items = self.request.session['order_items']
            for item in order_items:
                result.append(OrderItem.objects.create(product=Product.objects.get(pk=item), count=order_items[item]))
            return result
