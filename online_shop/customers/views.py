from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import HiddenInput
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView

from core.models import User
from customers.forms import UserForm, UserUpdateForm, CustomerUpdateForm
from customers.models import Customer
from orders.models import OrderItem, Order
from products.models import Product


class CustomerCreateView(CreateView):
    template_name = 'landing/html&css/html/pages/sign-up.html'
    form_class = UserForm
    success_url = reverse_lazy('products:products_list')

    def form_valid(self, form):
        response = super(CustomerCreateView, self).form_valid(form)
        Customer.objects.create(user=self.object)
        login(self.request, self.object)
        customer = Customer.objects.get(user_id=self.request.user.id)
        if order_items := self.request.session.get('order_items', []):
            for order_item in order_items:
                product = Product.objects.get(pk=order_item)
                OrderItem.objects.create(product=product, count=order_items[order_item], customer=customer)
        return response


class AboutTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'landing/html&css/html/pages/about.html'


class MyLoginView(LoginView):
    template_name = 'landing/html&css/html/pages/sign-in.html'

    def form_valid(self, form):
        validated_form = super().form_valid(form)
        customer = Customer.objects.get(user_id=self.request.user.id)
        if order_items := self.request.session.get('order_items', []):
            for order_item in order_items:
                try:
                    old_order_item = OrderItem.objects.get(customer=customer, product_id=order_item, status=0)
                    old_order_item.count += order_items[order_item]
                    old_order_item.save()
                except OrderItem.DoesNotExist:
                    product = Product.objects.get(pk=order_item)
                    OrderItem.objects.create(product=product, count=order_items[order_item], customer=customer)
        return validated_form


class CustomerDashboardTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'landing/html&css/html/pages/customer_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerDashboardTemplateView, self).get_context_data(**kwargs)
        context['unfinished_order_items'] = OrderItem.objects.filter(customer__user=self.request.user, status=0)
        context['unpaid_orders'] = Order.objects.filter(customer__user=self.request.user, pay_status=0)
        context['sending'] = Order.objects.filter(customer__user=self.request.user, sending_status=1)
        context['user_update_form'] = UserUpdateForm(instance=User.objects.get(pk=self.request.user.id))
        context['customer_update_form'] = CustomerUpdateForm(instance=Customer.objects.get(user=self.request.user))
        return context
