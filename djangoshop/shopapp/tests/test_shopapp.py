from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from shopapp.models import (CartModel, Categories, FeedbackModel, OrderModel,
                            Products, UserProfile)
from shopapp.views import *

# docker compose exec djangoshop-app python manage.py test --parallel
# shopapp.tests.test_shopapp.ShopAppTestCase.test_user_has_userprofile протестировать только метод
# python -m coverage run manage.py test
# python -m coverage report
# flake8 --append-config djangoshop/123.flake8 djangoshop

class ShopAppTestCase(TestCase):
    def setUp(self) -> None:
        # request Factory 
        self.factory = RequestFactory()

        # products
        self.product = Products(name='Тестовый продукт', product_code=8372156,
        description='''Описание товара на русском языке
        and in english language и много буквввввввввввввввввввввввввв''', price=12345678)
        self.product.save()
        categories = [Categories.objects.create(name='Смартфон'), Categories.objects.create(name='Телевизор')]
        self.product.categories.set(categories)

        # product 2
        self.product2 = Products(name='Тестовый продукт 2', product_code=12345,
        description='ыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыы', price=2222333)
        self.product2.save()
        self.product2.categories.add(categories[1])
        
        # categories
        self.categories = categories

        # feedback
        self.FEEDBACK_TEXT = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis et leo lorem. Sed maximus suscipit vestibulum. In sed commodo orci. Sed eget tellus lobortis, suscipit nibh vel, accumsan ex. Vestibulum mollis augue a nunc lobortis, id ornare mi luctus. Quisque at mauris nec massa dignissim faucibus. Duis vitae faucibus eros, in imperdiet neque. Fusce feugiat justo erat, eget vehicula arcu commodo eu. Nam pulvinar fringilla lacus. Ut eu risus neque. Vivamus tempus diam sit amet quam volutpat, at laoreet ante pharetra.
        Mauris ultricies urna non tempus aliquet. Donec a porttitor felis, sed lacinia nunc. Ut dictum viverra justo, vitae elementum libero tincidunt in. Morbi tortor libero, molestie eget viverra eu, varius at odio. Pellentesque ut erat nibh. Fusce dignissim metus turpis, ut congue nulla efficitur eu. Curabitur non ligula sed ante viverra finibus eu in sapien. Nam ac aliquet elit. Donec massa neque, facilisis vel elit in, posuere aliquet augue. Praesent auctor dui ut sagittis efficitur. Integer a viverra velit.
        Suspendisse malesuada semper leo, in tincidunt erat interdum non. Sed eget erat ut leo interdum lobortis. Proin a aliquet sem. Cras non accumsan orci. Nulla pretium neque quam, a consequat quam sollicitudin sit amet. Pellentesque sed iaculis elit, a aliquet urna. Nullam luctus felis at dui laoreet tincidunt. Suspendisse vitae nibh vel quam volutpat eleifend vitae in ante. Suspendisse cursus lorem enim, eu rhoncus dui eleifend sit amet. In commodo pellentesque ex, non efficitur quam. Morbi vehicula massa eget ipsum condimentum, at ornare dolor cursus.
        Sed eros elit, volutpat eu mollis sed, tincidunt id sem. Suspendisse potenti. Aliquam vel nisl volutpat, vulputate justo eu, mattis mi. Donec ultrices dignissim nibh, quis facilisis arcu finibus eget.
        Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nulla bibendum fermentum augue, eleifend pulvinar ipsum sollicitudin in. Sed scelerisque tellus.'''
        self.feedback = FeedbackModel.objects.create(name='Александр', text=self.FEEDBACK_TEXT, phone_number=+2131234578)

        # user
        self.admin_user = User.objects.create_user(username='admin', email='troshiy2011@mail.ru', password='admin', is_staff=True)
        self.user = User.objects.create_user(username='Alexander', email='troshiy2013@yandex.ru', password='123456', is_staff=False)
        
        # cart
        self.cart = CartModel.objects.get(user=self.user)

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

        return super().setUp()


    def test_products_model(self):
        self.assertEqual(self.product.get_absolute_url(), f'/product/{self.product.product_code}/')
        self.assertEqual(self.product.name, 'Тестовый продукт')
        self.assertEqual(list(self.product.categories.all()), list(self.categories))
        self.assertEqual(self.product.product_code, 8372156)
        self.assertEqual(self.product.description, '''Описание товара на русском языке
        and in english language и много буквввввввввввввввввввввввввв''')
        self.assertEqual(self.product.price, 12345678)
        self.assertEqual(self.product.image, None)

        self.assertEqual(self.product2.get_absolute_url(), f'/product/{self.product2.product_code}/')
        self.assertEqual(self.product2.name, 'Тестовый продукт 2')
        self.assertEqual(list(self.product2.categories.all())[0], list(self.categories)[1])
        self.assertEqual(self.product2.product_code, 12345)
        self.assertEqual(self.product2.description, 'ыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыыы')
        self.assertEqual(self.product2.price, 2222333)
        self.assertEqual(self.product2.image, None)

    def test_m2m(self):
        product3 = Products.objects.create(name='ТЕСТ ТЕСТ', product_code=123456,
        description='''Описание товара на русском языке
        and in english language и много буквввввввввввввввввввввввввв''', price=232323)
        product3.save()
        product3.categories.set(self.categories)

    def test_categories_model(self):
        self.assertEqual(Categories.objects.first().name, 'Смартфон')
        self.assertEqual(Categories.objects.last().name, 'Телевизор')

    def test_feedback_model(self):
        self.assertEqual(self.feedback.name, 'Александр')
        self.assertEqual(self.feedback.text, self.FEEDBACK_TEXT)
        self.assertEqual(self.feedback.phone_number, 2131234578)

    def test_admin_user(self):
        self.assertEqual(self.admin_user.username, 'admin')
        self.assertTrue(self.admin_user.is_staff)
        self.assertEqual(self.admin_user.email, 'troshiy2011@mail.ru')

    def test_user(self):
        self.assertEqual(self.user.username, 'Alexander')
        self.assertFalse(self.user.is_staff)
        self.assertEqual(self.user.email, 'troshiy2013@yandex.ru')
        self.assertEqual(self.user.userprofile.user.username, self.user.username)

    def test_user_has_cart(self):
        assert CartModel.objects.filter(user=self.user).exists()

    def test_user_has_userprofile(self):
        assert UserProfile.objects.filter(user=self.user).exists()

    def test_add_to_cart(self):
        self.cart.products.add(self.product)
        self.assertEqual(self.cart.products.all()[0], self.product)

    def test_remove_from_cart(self):
        self.cart.products.add(self.product)
        self.cart.products.remove(self.product)
        self.assertQuerysetEqual(self.cart.products.all(), Products.objects.none())

    def test_order(self):
        self.assertEqual(self.order.user.username, 'Alexander')
        self.assertEqual(self.order.products.first(), self.product)
        self.assertEqual(self.order.total_price, self.product.price)
        self.assertEqual(self.order.order_id, 1)
        product_price_sum = sum(i.price for i in self.order.products.all())
        self.assertEqual(self.order.total_price, product_price_sum)
        self.assertEqual(OrderModel.objects.get(order_id=1).total_price, product_price_sum)

        self.assertEqual(self.order2.user.username, 'Alexander')
        self.assertEqual(self.order2.products.all()[0], self.product)
        self.assertEqual(self.order2.products.all()[1], self.product2)
        self.assertEqual(self.order2.total_price, self.product.price + self.product2.price)
        self.assertEqual(self.order2.order_id, 2)
        product2_price_sum = sum(i.price for i in self.order2.products.all())
        self.assertEqual(self.order2.total_price, product2_price_sum)
        self.assertEqual(OrderModel.objects.get(order_id=2).total_price, product2_price_sum)

    def test_create_order_model_function(self):
        self.cart.products.set((self.product,self.product2))
        self.assertEqual(self.cart.products.all()[0], self.product)
        self.assertEqual(self.cart.products.all()[1], self.product2)
        request = self.factory.post('cart/order/')
        request.user = self.user
        response = OrderView.as_view()(request)
        self.assertFalse(self.cart.products.exists())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.cart.products.count(), 0)
        self.assertEqual(self.user.userprofile.orders.count(), 3)

    def test_user_profile_orders(self):
        self.assertEqual(self.user.userprofile.orders.count(), 2)

    def test_views(self):
        request = self.factory.get('/cart/')
        request.user = self.user
        response = CartView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
        request = self.factory.get('cart/')
        request.user = AnonymousUser()
        response = CartView.as_view()(request)
        self.assertEqual(response.status_code, 302)

    # users = User.objects.values('is_staff').annotate(count=Count('id')) # Group by количество всех is_staff и не стафф юзеров
    # print(users)
    # print(users.query)
