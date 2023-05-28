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
    # context_test = serializers.SerializerMethodField()

    # def get_context_test(self, context):
    #     print(self.context)
    #     return self.context

    class Meta:
        model = OrderModel
        fields = '__all__'
        extra_kwargs = {'total_price': {'required': False, 'read_only': True},
                        'order_id': {'required': False, 'read_only': True},}

class OrderListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductsSerializer(many=True, read_only=True)

    class Meta:
        model = OrderModel
        fields = '__all__'