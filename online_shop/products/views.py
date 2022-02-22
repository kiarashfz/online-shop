from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, CreateView, DetailView

from products.models import Product, Brand, Category
from products.serializers import ProductSerializer


class ProductListView(TemplateView):
    template_name = 'landing/html&css/html/pages/pricing.html'

    def get_context_data(self, **kwargs):
        extra_context = {
            'brands': Brand.objects.all(),
            'categories': Category.objects.all(),
        }
        return extra_context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'landing/html&css/html/pages/product_detail.html'


#
# @csrf_exempt
# def product_list_api(request):
#     if request.method == 'GET':
#         product_serializer = ProductSerializer(Product.objects.all(), many=True)
#         return JsonResponse({'data': product_serializer.data}, status=200)
#
#     elif request.method == 'POST':
#         data = request.POST
#         product_serializer = ProductSerializer(data=data)
#         if product_serializer.is_valid():
#             new_product = product_serializer.save()
#             return JsonResponse({'new_product_id': new_product.id}, status=201)
#         else:
#             return JsonResponse({'errors': product_serializer.errors}, status=400)
#     else:
#         return JsonResponse({}, status=405)
