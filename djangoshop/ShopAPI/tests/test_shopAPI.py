from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from shopapp.models import Products, CartModel, Categories, OrderModel
from django.contrib.auth.models import User, AnonymousUser
from ShopAPI.serializers import ProductsSerializer, OrderSerializer, CartSerializer


# docker compose exec djangoshop-app python manage.py test
# shopapp.tests.test_shopapp.ShopAppTestCase.test_user_has_userprofile протестировать только метод
# python -m coverage run manage.py test
# python -m coverage report


class ShopAPITestCase(APITestCase):
    def setUp(self) -> None:

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
        self.url_detail_carts = reverse('carts-detail', args=[CartModel.objects.first().id])
        self.url_detail_orders = reverse('orders-detail', args=[Products.objects.first().id])

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


# TODO test login register serializers and POSTs
# teso