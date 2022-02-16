from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
