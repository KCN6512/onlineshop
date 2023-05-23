from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models, transaction
from django.http import HttpResponse
from django.urls import reverse

from .mixins import *


class Products(models.Model):
    name = models.CharField('Название', max_length=128)
    product_code = models.PositiveIntegerField('Код продукта', unique=True,
                                               validators=[MaxValueValidator(9999999)])
    description = models.TextField('Описание товара',
                                   default='Тестовое описание товара',
                                   blank=True)
    price = models.DecimalField('Цена за единицу', max_digits=10, decimal_places=2)
    categories = models.ManyToManyField('Categories', related_name='products')
    image = models.ImageField(null=True, upload_to='%Y/%d/%m/')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("product", kwargs={"product_code": self.product_code})

    class Meta:
        ordering = ['-price']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Categories(models.Model):
    name = models.CharField('Название категории', max_length=20)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class FeedbackModel(models.Model):
    name = models.CharField('Ваше имя', max_length=20)
    text = models.TextField(verbose_name='Ваше сообщение')
    phone_number = models.CharField('Ваш телефонный номер', max_length=12,
                                    validators=[RegexValidator(regex=r'^\+?1?\d{9,11}$')])

    def __str__(self) -> str:
        return f'{self.name} {self.phone_number}'

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'


class CartModel(models.Model, PriceSummaryMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    products = models.ManyToManyField(Products, verbose_name='Товары')

    def __str__(self):
        return f'{self.user.username} "корзина"'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class OrderModel(models.Model, PriceSummaryMixin):
    def get_order_id():
        last_order = OrderModel.objects.last()
        if not last_order:
            return 1
        return last_order.order_id + 1

    @transaction.atomic
    def create_order(request):
        cart = CartModel.objects.prefetch_related('products').get(user=request.user)
        products = cart.products.all()
        order = OrderModel(user=request.user, total_price=0)
        order.save()
        order.products.set(products)
        if not order.products.exists():
            return HttpResponse('<h1>Заказ пуст, продолжение невозможно</h1>')
        order.total_price = order.price_summary()
        order.save()
        # Удаление купленных товаров из корзины
        items_to_remove = [i for i in cart.products.all()]
        cart.products.remove(*items_to_remove)

    user = models.ForeignKey(User, verbose_name='покупатель',
                             on_delete=models.CASCADE, blank=False,
                             null=True)
    order_id = models.PositiveIntegerField('Номер заказа', unique=True,
                                           default=get_order_id)
    products = models.ManyToManyField(Products, verbose_name='Товары в заказе')
    date = models.DateTimeField('Дата заказа', auto_now=True)
    total_price = models.DecimalField('Итоговая цена заказа', max_digits=15,
                                      decimal_places=2,
                                      null=False)

    def __str__(self):
        return f'{self.user} {self.order_id } {self.date} {self.total_price}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['date']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(OrderModel, related_name='orders')
    cart = models.OneToOneField(CartModel, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.user} профиль'

    def get_absolute_url(self):
        return reverse("product_category", kwargs={"category_name": self.name})

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили'
# transaction.atomic() блокирует изменение записи в бд пока активны другие транзакции и ждет их освобождения
# так же нужен select_for_update() блокирующий изменения
