from pprint import pprint

from django.db.models import Count
from rest_framework import mixins, generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from products.models import Product, Category, Discount, OffCode, Property, Comment
from products.serializers import ProductSerializer, CategorySerializer, DiscountSerializer, OffCodeSerializer, \
    PropertySerializer, CommentSerializer


# class MyPaginator(PageNumberPagination):
#     page_size = 5


class ProductListApiView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.annotate(orderitem_count=Count('orderitem')).order_by('-orderitem_count')[:9]
    pagination_class = PageNumberPagination

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.GET.get('category', False) and request.GET['category'] != 'All':
            queryset = queryset.filter(category__name=request.GET['category'])
        if request.GET.get('brand', False) and request.GET['brand'] != 'All':
            queryset = queryset.filter(brand__name=request.GET['brand'])
        if request.GET.get('min_price', False):
            queryset = queryset.filter(final_price__gte=request.GET['min_price'])
        if request.GET.get('max_price', False):
            queryset = queryset.filter(final_price__lte=request.GET['max_price'])
        queryset = self.paginate_queryset(queryset)
        serializer = ProductSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)


class CategoryProductsListApiView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['category_id'])
        categories = category.get_all_children()
        return super(CategoryProductsListApiView, self).get_queryset().filter(category__in=categories)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.GET.get('category', False) and request.GET['category'] != 'All':
            queryset = queryset.filter(category__name=request.GET['category'])
        if request.GET.get('brand', False) and request.GET['brand'] != 'All':
            queryset = queryset.filter(brand__name=request.GET['brand'])
        if request.GET.get('min_price', False):
            queryset = queryset.filter(final_price__gte=request.GET['min_price'])
        if request.GET.get('max_price', False):
            queryset = queryset.filter(final_price__lte=request.GET['max_price'])
        queryset = self.paginate_queryset(queryset)
        serializer = ProductSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     paginated_products = self.paginate_queryset(queryset)
    #     paginated_products_ids = []
    #     for product in paginated_products:
    #         paginated_products_ids.append(product.id)
    #     queryset = Product.objects.filter(pk__in=paginated_products_ids)
    #     if request.GET.get('category', False) and request.GET['category'] != 'All':
    #         queryset = queryset.filter(category__name=request.GET['category'])
    #     if request.GET.get('brand', False) and request.GET['brand'] != 'All':
    #         queryset = queryset.filter(brand__name=request.GET['brand'])
    #     if request.GET.get('min_price', False):
    #         queryset = queryset.filter(final_price__gte=request.GET['min_price'])
    #     if request.GET.get('max_price', False):
    #         queryset = queryset.filter(final_price__lte=request.GET['max_price'])
    #     serializer = ProductSerializer(queryset, many=True)
    #     return self.get_paginated_response(serializer.data)


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CategoryListApiView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class DiscountListApiView(generics.ListCreateAPIView):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()


class DiscountDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()


class OffCodeListApiView(generics.ListCreateAPIView):
    serializer_class = OffCodeSerializer
    queryset = OffCode.objects.all()


class OffCodeDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OffCodeSerializer
    queryset = OffCode.objects.all()


class PropertyListApiView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    queryset = Product.objects.all()


class PropertyDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()


class CommentCreateApiView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
