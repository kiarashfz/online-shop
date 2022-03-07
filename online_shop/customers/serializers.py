from rest_framework import serializers

from core.models import User
from customers.models import Customer, Address


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    customer = serializers.HyperlinkedRelatedField(view_name='customers:user_detail_api_view', read_only=True)
    complete_province = serializers.CharField(source='get_province_display', read_only=True)
