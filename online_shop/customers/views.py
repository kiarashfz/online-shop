from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView

from core.models import User
from customers.forms import UserForm
from customers.models import Customer


class CustomerCreateView(CreateView):
    template_name = 'landing/html&css/html/pages/sign-up.html'
    form_class = UserForm
    success_url = reverse_lazy('products:products_list')

    def form_valid(self, form):
        response = super(CustomerCreateView, self).form_valid(form)
        Customer.objects.create(user=self.object)
        login(self.request, self.object)
        return response


class AboutTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'landing/html&css/html/pages/about.html'

