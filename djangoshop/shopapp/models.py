from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Products(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    product_code = models.PositiveIntegerField(unique=True,validators=[MaxValueValidator(9999999)], verbose_name='Код продукта')
    description = models.TextField(verbose_name='Описание товара',default='Тестовое описание товара', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    categories = models.ManyToManyField('Categories', related_name='products')
    image = models.ImageField(null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("product", kwargs={"product_code": self.product_code})
    
    class Meta:
        ordering = ['-price']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Categories(models.Model):
    name = models.CharField(max_length=20)

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
    phone_number = models.CharField(max_length=12, verbose_name='Ваш телефонный номер')

    def __str__(self) -> str:
        return f'{self.name} {self.phone_number}'
        
    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'


class CartModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField(Products, verbose_name='Товары')

    def __str__(self):
        return self.user.username + ' ' 'корзина'

    def price_summary(self):
        return f"{self.products.all().aggregate(models.Sum('price'))['price__sum']:.2f}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class OrderModel(models.Model):#сделать миграцию
    user = models.ForeignKey(User, verbose_name='покупатель', on_delete=models.CASCADE)
    order_id = models.PositiveIntegerField(unique=True, null=True, verbose_name='номер заказа')
    products = models.ManyToManyField(Products, verbose_name='номер заказа')
    date = models.DateTimeField(auto_now=True)
    
    def price_summary(self):
        return f"{self.products.all().aggregate(models.Sum('price'))['price__sum']:.2f}"
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(OrderModel, related_name='orders')
    cart = models.OneToOneField(CartModel, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f'{self.user} профиль'
        
    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили'
