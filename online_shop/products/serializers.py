from rest_framework import serializers

from .models import Product, Brand, Category, Discount, Property, OffCode, CustomerOffCode, Comment


# class PropertySerializer(serializers.Serializer):
#     key = serializers.CharField(max_length=255)
#     value = serializers.CharField(max_length=2555)
#
#     def create(self, validated_data):
#         return Property.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.key = validated_data.get('key', instance.key)
#         instance.value = validated_data.get('value', instance.value)
#         return instance


# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=31, required=True)
#     price = serializers.IntegerField(min_value=0)
#     brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
#     # image = serializers.ImageField()
#     properties = serializers.PrimaryKeyRelatedField(queryset=Property.objects.all(), many=True)
#     stock = serializers.IntegerField(min_value=0)
#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     discount = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all(), allow_null=True)
#
#     def create(self, validated_data):
#         return Product.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.price = validated_data.get('name', instance.price)
#         instance.brand = validated_data.get('name', instance.brand)
#         instance.image = validated_data.get('image', instance.image)
#         # instance.properties = validated_data.get('name', instance.properties)
#         instance.stock = validated_data.get('stock', instance.stock)
#         instance.category = validated_data.get('stock', instance.category)
#         instance.discount = validated_data.get('stock', instance.discount)
#         return instance

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    brand_name = serializers.CharField(source='brand.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class OffCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OffCode
        fields = '__all__'


class CustomerOffCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOffCode
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
