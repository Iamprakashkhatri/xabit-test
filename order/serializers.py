from django.db.models import Avg
from rest_framework import serializers

from .models import OrderProduct, Order

class OrderProductSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderProduct
        fields = "__all__"

    def get_product_name(self, obj):
        return obj.product.name

class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"