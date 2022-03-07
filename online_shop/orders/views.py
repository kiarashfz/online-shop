from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, QueryDict, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from customers.forms import AddressForm
from customers.models import Customer, Address
from orders.models import OrderItem, Order
from products.models import Product
from products.templatetags.product_extras import toman_format


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
        order_item = OrderItem(product=Product.objects.get(id=int(data['product_id'])), count=int(data['count']))
        order_item.final_price = order_item.final_price_calculator()
        price = order_item.price_formatter()
        order_items = request.session['order_items']
        order_items_final_price = 0
        for order_item in order_items:
            new_order_item = OrderItem(product=Product.objects.get(id=int(order_item)), count=int(order_items[order_item]))
            new_order_item.final_price = new_order_item.final_price_calculator()
            order_items_final_price += new_order_item.final_price
        order_items_final_price = intcomma(toman_format(order_items_final_price))
        return JsonResponse({'formatted_price': price, 'final_prices_sum': order_items_final_price})

    def delete(self, request):
        data = QueryDict(request.body)
        del request.session['order_items'][data['product_id']]
        request.session['order_items'] = request.session['order_items']
        return HttpResponse('ok')


class OrderItemListView(ListView):
    model = OrderItem
    template_name = 'landing/html&css/html/pages/order_items_list.html'

    def get_queryset(self):
        if self.request.user.id:
            return OrderItem.objects.filter(customer__user=self.request.user, status=0)
        else:
            if self.request.session.get('order_items', None):
                result = []
                session_order_items = self.request.session['order_items']
                id_creator = 1
                for order_item in session_order_items:
                    product = Product.objects.get(pk=order_item)
                    new_order_item = OrderItem(product=product, count=session_order_items[order_item])
                    new_order_item.final_price = new_order_item.product.final_price * new_order_item.count
                    new_order_item.id = id_creator
                    id_creator += 1
                    result.append(new_order_item)
                return result

    def get_context_data(self, **kwargs):
        context = super(OrderItemListView, self).get_context_data(**kwargs)
        if self.get_queryset():
            if self.request.user.id:
                context['final_price'] = sum(self.get_queryset().values_list('final_price', flat=True))
                return context
            else:
                final_price = 0
                for item in self.get_queryset():
                    final_price += item.final_price
                context['final_price'] = final_price
                return context


class OrderCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Order
    template_name = 'landing/html&css/html/pages/order_create.html'
    success_url = reverse_lazy('products:products_list')
    success_message = 'Thank for choosing Web Mall!'
    fields = ['address', 'off_code']

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['form'].fields['address'].queryset = Address.objects.filter(customer__user=self.request.user)
        context['addresses'] = Address.objects.filter(customer__user=self.request.user)
        context['address_form'] = AddressForm()
        return context

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(user=self.request.user)
        validated_form = super(OrderCreateView, self).form_valid(form)
        OrderItem.objects.filter(customer__user=self.request.user, status=0).update(status=1, order=self.object)
        self.object.save()
        return validated_form

    def get_form_kwargs(self):
        kwargs = super(OrderCreateView, self).get_form_kwargs()
        if kwargs['instance'] is None:
            kwargs['instance'] = Order()
        kwargs['instance'].customer = Customer.objects.get(user=self.request.user)
        return kwargs
