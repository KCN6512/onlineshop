from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    product_code = models.PositiveIntegerField(unique=True, validators=[MaxValueValidator(9999999)], verbose_name='Код продукта')
    description = models.TextField(verbose_name='Описание товара',default='Тестовое описание товара', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    categories = models.ManyToManyField('Categories', related_name='products')
    image = models.ImageField(null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("product", kwargs={"product_code": self.product_code})
    
    class Meta:
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


# class Order:
#     pass

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

class FeedbackModel(models.Model):
    name = models.CharField(max_length=20)
    text = models.TextField()
    phone_number = models.CharField(max_length=12)