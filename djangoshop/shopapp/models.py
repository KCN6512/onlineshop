from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse

# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    product_code = models.PositiveIntegerField(unique=True, validators=[MaxValueValidator(9999999)], verbose_name='Код продукта') # семизначное число
    description = models.TextField(verbose_name='Описание товара')
    price = models.DecimalField(max_digits=10000000000, decimal_places=2, verbose_name='Цена за единицу')
    categories = models.ManyToManyField('Categories', related_name='categories')
    image = models.ImageField(null=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse("product", kwargs={"code": self.product_code})
    

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Categories(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Order:
    pass