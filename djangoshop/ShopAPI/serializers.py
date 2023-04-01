from django.contrib.auth.models import User
from rest_framework import serializers
from shopapp.models import *


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = OrderModel
        fields = '__all__'
        extra_kwargs = {'total_price': {'required': False, 'read_only': True},
                        'order_id': {'required': False, 'read_only': True},}
