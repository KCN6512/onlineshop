from django.test import TestCase
from shopapp.models import CartModel, OrderModel, Products, Categories, FeedbackModel
from shopapp.permissions import IsOwnerOrReadOnly
from shopapp.serializers import (CartSerializer, OrderSerializer,
                                 ProductsSerializer)
from django.contrib.auth.models import User
# python manage.py test
# docker compose exec djangoshop-app python manage.py test
class ShopAppTestCase(TestCase):
    def setUp(self) -> None:
        # products
        self.product = Products(name='Тестовый продукт', product_code=8372156,
        description='''Описание товара на русском языке
        and in english language и много буквввввввввввввввввввввввввв''', price=12345678)
        self.product.save()
        categories = [Categories.objects.create(name='Смартфон'), Categories.objects.create(name='Телевизор')]
        self.product.categories.set(categories)
        self.product.save()

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
        return super().setUp()

    def test_products_model(self):
        self.assertEqual(self.product.get_absolute_url(), f'/product/{self.product.product_code}/')
        self.assertEqual(self.product.name, 'Тестовый продукт')
        self.assertEqual(list(self.product.categories.all()), list(self.categories))
        self.assertEqual(self.product.product_code, 8372156)
        self.assertEqual(self.product.description, '''Описание товара на русском языке
        and in english language и много буквввввввввввввввввввввввввв''')
        self.assertEqual(self.product.product_code, 8372156)
        self.assertEqual(self.product.price, 12345678)
        self.assertEqual(self.product.image, None)

    def test_categories_model(self):
        self.assertEqual(Categories.objects.first().name, 'Смартфон')
        self.assertEqual(Categories.objects.last().name, 'Телевизор')

    def test_feedback_model(self):
        self.assertEqual(self.feedback.name, 'Александр')
        self.assertEqual(self.feedback.text, self.FEEDBACK_TEXT)
        self.assertEqual(self.feedback.phone_number, 2131234578)

    def test_admin_user(self):
        self.assertEqual(self.admin_user.username, 'admin')
        self.assertEqual(self.admin_user.is_staff, True)
        self.assertEqual(self.admin_user.email, 'troshiy2011@mail.ru')

    def test_user(self):
        self.assertEqual(self.user.username, 'Alexander')
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.email, 'troshiy2013@yandex.ru')
        self.assertEqual(self.user.userprofile.user.username, self.user.username)

#cart order