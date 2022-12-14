# Generated by Django 4.1.2 on 2022-10-18 12:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0003_categories_products_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_code',
            field=models.PositiveIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(9999999)], verbose_name='Код продукта'),
        ),
    ]
