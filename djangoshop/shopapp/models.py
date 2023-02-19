from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.urls import reverse


class Products(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    product_code = models.PositiveIntegerField(unique=True,
    validators=[MaxValueValidator(9999999)], verbose_name='Код продукта')
    description = models.TextField(verbose_name='Описание товара',
    default='Тестовое описание товара', blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, 
                                verbose_name='Цена за единицу')
    categories = models.ManyToManyField('Categories', related_name='products')
    image = models.ImageField(null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("product", kwargs={"product_code": self.product_code})
    
    class Meta:
        ordering = ['-price']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Categories(models.Model):
    name = models.CharField(max_length=20, verbose_name='Игровая консоль')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("product_category", kwargs={"category_name": self.name})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class FeedbackModel(models.Model):
    name = models.CharField(max_length=20, verbose_name='Ваше имя')
    text = models.TextField(verbose_name='Ваше сообщение')
    phone_number = models.CharField(max_length=12, verbose_name='Ваш телефонный номер', 
                                    validators=[RegexValidator(regex=r'^\+?1?\d{9,11}$')])

    def __str__(self) -> str:
        return f'{self.name} {self.phone_number}'
        
    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'


class CartModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                               verbose_name='Пользователь')
    products = models.ManyToManyField(Products, verbose_name='Товары')

    def __str__(self):
        return f'{self.user.username} "корзина"'

    def price_summary(self):
        price = self.products.all().aggregate(models.Sum('price')).get('price__sum')
        return price

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class OrderModel(models.Model):
    def get_order_id():
        last_order = OrderModel.objects.all().last()
        if not last_order:
            return 1
        return last_order.id + 1

    user = models.ForeignKey(User, verbose_name='покупатель',
    on_delete=models.CASCADE, blank=False, null=True)
    order_id = models.PositiveIntegerField(unique=True, default=get_order_id,
                                          verbose_name='Номер заказа')
    products = models.ManyToManyField(Products, verbose_name='Товары в заказе')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата заказа')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, 
                  verbose_name='Итоговая цена заказа', null=False)

    def __str__(self):
        return f'{self.user} {self.order_id } {self.date}'
    
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
        
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили'
