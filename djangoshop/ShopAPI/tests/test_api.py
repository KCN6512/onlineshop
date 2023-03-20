from django.test import TestCase
from shopapp.models import CartModel, OrderModel, Products
from shopapp.permissions import IsOwnerOrReadOnly
from shopapp.serializers import (CartSerializer, OrderSerializer,
                                 ProductsSerializer)
# python manage.py test
class APITestCase(TestCase):
    def test_products_model(self):
        product = Products.objects.create()
        