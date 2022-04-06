from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, CreateView, DetailView

from products.models import Product, Brand, Category, Comment
from products.serializers import ProductSerializer
from company.models import Question


class ProductListView(TemplateView):
    template_name = 'landing/html&css/html/pages/pricing.html'

    def get_context_data(self, **kwargs):
        extra_context = {
            'brands': Brand.objects.all(),
            'questions': Question.objects.all()
        }
        return extra_context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'landing/html&css/html/pages/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(category=self.object.category).exclude(pk=self.object.id)
        context['parent_comments'] = Comment.objects.filter(parent=None, product=self.object)
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'landing/html&css/html/pages/category_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brands'] = Brand.objects.filter(categories__name__contains=self.object.name)
        return context

    # def get_queryset(self):
    #     category = Category.objects.get(pk=self.kwargs['category_id'])
    #     categories = category.get_all_children()
    #     return super(CategoryProductsListView, self).get_queryset().filter(category__in=categories)


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
