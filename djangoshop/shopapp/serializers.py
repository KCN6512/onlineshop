from rest_framework import serializers

from .models import *


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    categories = CategoriesSerializer(many=True) #для полного вывода всех полей категории
    request_user = serializers.CharField(default=serializers.CurrentUserDefault())
        # Create a custom method field

    class Meta:
        model = Products
        fields = '__all__'
#все в виде api 

