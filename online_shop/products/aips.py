from rest_framework import mixins, generics
from rest_framework.response import Response

from products.models import Product, Category, Discount, OffCode, Property
from products.serializers import ProductSerializer, CategorySerializer, DiscountSerializer, OffCodeSerializer, \
    PropertySerializer


class ProductListApiView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if request.GET.get('category', False) and request.GET['category'] != 'All':
            queryset = queryset.filter(category__name=request.GET['category'])
        if request.GET.get('brand', False)  and request.GET['brand'] != 'All':
            queryset = queryset.filter(brand__name=request.GET['brand'])
        if request.GET.get('min_price', False):
            queryset = queryset.filter(final_price__gte=request.GET['min_price'])
        if request.GET.get('max_price', False):
            queryset = queryset.filter(final_price__lte=request.GET['max_price'])
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


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
