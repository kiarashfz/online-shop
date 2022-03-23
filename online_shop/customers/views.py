from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.forms import HiddenInput
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView

from core.models import User
from customers.forms import UserForm, UserUpdateForm, CustomerUpdateForm, AddressForm
from customers.models import Customer, Address
from orders.models import OrderItem, Order
from products.models import Product


class CustomerCreateView(CreateView):
    template_name = 'landing/html&css/html/pages/sign-up.html'
    form_class = UserForm
    success_url = reverse_lazy('customers:dashboard')

    def get_initial(self):
        init = super(CustomerCreateView, self).get_initial()
        init.update({'request': self.request})
        return init

    def form_valid(self, form):
        response = super(CustomerCreateView, self).form_valid(form)
        Customer.objects.create(user=self.object)
        login(self.request, self.object)
        customer = Customer.objects.get(user_id=self.request.user.id)
        if order_items := self.request.session.get('order_items', []):
            inited_objs = []
            for order_item in order_items:
                product = Product.objects.get(pk=order_item)
                inited_objs.append(OrderItem(product=product, count=order_items[order_item], customer=customer))
            OrderItem.objects.bulk_create(inited_objs)
            # for order_item in order_items:
            #     product = Product.objects.get(pk=order_item)
            #     OrderItem.objects.create(product=product, count=order_items[order_item], customer=customer)
        return response

    def form_invalid(self, form):
        if self.request.session['confirm_code']:
            del self.request.session['confirm_code']
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CustomerCreateView, self).get_context_data(**kwargs)
        context['confirm_code'] = self.request.session.get('confirm_code', None)
        return context


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
        context['unfinished_order_items'] = OrderItem.objects.filter(customer__user=self.request.user, status=0).order_by('-created')
        context['unpaid_orders'] = Order.objects.filter(customer__user=self.request.user, pay_status=0).order_by('-created')
        context['sending_orders'] = Order.objects.filter(customer__user=self.request.user, sending_status=1).order_by('-created')
        context['finished_orders'] = Order.objects.filter(customer__user=self.request.user, sending_status=2).order_by('-created')
        context['user_update_form'] = UserUpdateForm(instance=User.objects.get(pk=self.request.user.id))
        context['customer_update_form'] = CustomerUpdateForm(instance=Customer.objects.get(user=self.request.user))
        context['addresses'] = Address.objects.filter(customer__user=self.request.user).order_by('-created')
        context['address_form'] = AddressForm()
        return context
