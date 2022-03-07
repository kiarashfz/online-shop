from rest_framework import serializers

from orders.models import Order, OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

    formatted_price = serializers.CharField(source='price_formatter', read_only=True)
    final_prices_sum = serializers.CharField(source='order_items_final_price', read_only=True)
