from rest_framework import serializers

from .models import *


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartModel
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    # total_price_method_field = serializers.SerializerMethodField()

    # def get_total_price_method_field(self, instance):
    #     return instance.annotated_price # берется из annotate

    class Meta:
        model = OrderModel
        fields = '__all__'
