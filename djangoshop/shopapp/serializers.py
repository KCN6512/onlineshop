from rest_framework import serializers

from .models import *


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    #categories = CategoriesSerializer(many=True)

    class Meta:
        model = Products
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    #products = ProductsSerializer(many=True)

    class Meta:
        model = CartModel
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    #products = ProductsSerializer(many=True)
    class Meta:
        model = OrderModel
        fields = '__all__'
