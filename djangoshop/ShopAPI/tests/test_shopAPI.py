import json

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from ShopAPI.serializers import (CartSerializer, OrderSerializer,
                                 ProductsSerializer)
from ShopAPI.views import OrderViewSet
from shopapp.models import CartModel, Categories, OrderModel, Products

# docker compose exec djangoshop-app python manage.py test
# shopapp.tests.test_shopapp.ShopAppTestCase.test_user_has_userprofile протестировать только метод
# python -m coverage run manage.py test
# python -m coverage report


class ShopAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        # products
        self.product = Products(name='Тестовый продукт', product_code=8372156,
        description='''Описание товара на русском языке
        and in english language и много буквввввввввввввввввввввввввв''', price=12345678)
        self.product.save()
        # categories
        self.categories = [Categories.objects.create(name='Смартфон'), Categories.objects.create(name='Телевизор')]
        self.product.categories.set(self.categories)
        # product 2
        self.product2 = Products(name='Тестовый продукт 2', product_code=12345,
        description='ыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыы', price=2222333)
        self.product2.save()
        self.product2.categories.add(self.categories[1])
        # s
        self.admin_user = User.objects.create_user(username='admin', email='troshiy2011@mail.ru', password='admin', is_staff=True)
        self.user = User.objects.create_user(username='Alexander', email='troshiy2013@yandex.ru', password='123456', is_staff=False)
        self.anon_user = AnonymousUser()
        # cart
        #self.cart = CartModel.objects.get(user=self.user)
        # urls
        self.url_products = reverse('products-list')
        self.url_carts = reverse('carts-list')
        self.url_orders = reverse('orders-list')
        # urls details
        self.url_detail_products = reverse('products-detail', args=[Products.objects.first().id])

        # order
        self.order = OrderModel.objects.create(user=self.user, total_price=0)
        self.order.save()
        self.order.products.add(self.product)
        self.order.total_price = self.order.price_summary()
        self.order.save()

        # order 2
        self.order2 = OrderModel.objects.create(user=self.user, total_price=0)
        self.order2.save()
        self.order2.products.set((self.product, self.product2))
        self.order2.total_price = self.order2.price_summary()
        self.order2.save()
        # products json
        self.products = {"products": [1]}
        return super().setUp()
    
    def test_is_user_staff(self):
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.admin_user.is_staff, True)
        self.assertEqual(self.anon_user.is_staff, False)

    # get products
    def test_get_products_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url_products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.user)

    def test_get_products_admin_user(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.admin_user)

    def test_get_products_anon_user(self):
        response = self.client.get(self.url_products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.anon_user)

    # get carts
    def test_get_carts_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url_carts)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.user)

    def test_get_carts_admin_user(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_carts)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.admin_user)

    def test_get_carts_anon_user(self):
        response = self.client.get(self.url_carts)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.anon_user)

    # get orders
    def test_get_orders_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url_orders)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.user)

    def test_get_orders_admin_user(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_orders)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.admin_user)

    def test_get_orders_anon_user(self):
        response = self.client.get(self.url_orders)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.anon_user)

    def test_get_recent_orders(self):
        view = OrderViewSet.as_view(actions={'get': 'recent_orders'})
        request = self.factory.get(f'/api/v1/orders/recent_orders/')
        response = view(request)
        serializer = OrderSerializer(OrderModel.objects.all().order_by('-date')[:10], many=True)
        self.assertEqual(response.data['recent orders'], serializer.data) 

    # get single product 
    def test_get_product_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(self.url_detail_products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.user)
        # serializer data
        serializer = ProductsSerializer(Products.objects.get(id=self.product.id))
        self.assertEqual(response.data, serializer.data)

    def test_get_product_admin_user(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(self.url_detail_products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.admin_user)
        # serializer data
        serializer = ProductsSerializer(Products.objects.get(id=self.product.id))
        self.assertEqual(response.data, serializer.data)

    def test_get_product_anon_user(self):
        response = self.client.get(self.url_detail_products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.anon_user)
        # serializer data
        serializer = ProductsSerializer(Products.objects.get(id=self.product.id))
        self.assertEqual(response.data, serializer.data)

    # get single cart
    def test_get_cart_user(self):
        self.client.force_login(user=self.user)
        response = self.client.get(reverse('carts-detail', args=[self.user.userprofile.cart.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.user)
        # serializer data
        serializer = CartSerializer(CartModel.objects.get(id=self.user.userprofile.cart.id))
        self.assertEqual(response.data, serializer.data)

    def test_get_cart_admin_user(self):
        self.client.force_login(user=self.admin_user)
        response = self.client.get(reverse('carts-detail', args=[self.admin_user.userprofile.cart.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.wsgi_request.user, self.admin_user)
        # serializer data
        serializer = CartSerializer(CartModel.objects.get(id=self.admin_user.userprofile.cart.id))
        self.assertEqual(response.data, serializer.data)


    def test_get_cart_anon_user(self):
        self.assertRaises(AttributeError, lambda: self.client.get(reverse('carts-detail', args=[self.anon_user.userprofile.cart.id])))
        self.assertRaises(AttributeError, lambda: CartSerializer(CartModel.objects.get(id=self.anon_user.userprofile.cart.id)))

    def test_post_product(self):
        # user
        self.client.force_login(user=self.user)
        response = self.client.post('/api/v1/products/')
        response2 = self.client.post(reverse('products-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response2.status_code, status.HTTP_403_FORBIDDEN)
        # admin_user   
        self.client.force_login(user=self.admin_user)
        response = self.client.post(reverse('products-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

# need token
    # def test_post_orders(self):
    #     # user
    #     self.client.force_login(user=self.user)
    #     response = self.client.post(reverse('orders-list'))
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     # admin_user   
    #     self.client.force_login(user=self.admin_user)
    #     response = self.client.post(reverse('orders-list'))
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #     # user
    #     self.client.force_login(user=self.user)
    #     request = self.factory.post(reverse('orders-list'), data=json.dumps(self.products), content_type='application/json', )
    #     view = OrderViewSet.as_view(actions={'post': 'create'})
    #     response = view(request)
    #     print(response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
