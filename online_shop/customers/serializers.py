from rest_framework import serializers

from core.models import User
from customers.models import Customer, Address
from products.models import Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def update(self, instance, validated_data):
        if not validated_data['image']:
            validated_data['image'] = 'customers/default_customer.png'
        return super(CustomerSerializer, self).update(instance, validated_data)


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    customer = serializers.HyperlinkedRelatedField(view_name='customers:user_detail_api_view', read_only=True)
    complete_province = serializers.CharField(source='get_province_display', read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
