# Generated by Django 4.1.2 on 2023-02-12 12:17

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import shopapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CartModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='FeedbackModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Ваше имя')),
                ('text', models.TextField(verbose_name='Ваше сообщение')),
                ('phone_number', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex='^\\+?1?\\d{9,11}$')], verbose_name='Ваш телефонный номер')),
            ],
            options={
                'verbose_name': 'Обратная связь',
                'verbose_name_plural': 'Обратная связь',
            },
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.PositiveIntegerField(default=shopapp.models.OrderModel.get_order_id, unique=True, verbose_name='Номер заказа')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата заказа')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='shopapp.cartmodel')),
                ('orders', models.ManyToManyField(related_name='orders', to='shopapp.ordermodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('product_code', models.PositiveIntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(9999999)], verbose_name='Код продукта')),
                ('description', models.TextField(blank=True, default='Тестовое описание товара', verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена за единицу')),
                ('image', models.ImageField(null=True, upload_to='')),
                ('categories', models.ManyToManyField(related_name='products', to='shopapp.categories')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-price'],
            },
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='products',
            field=models.ManyToManyField(to='shopapp.products', verbose_name='Товары в заказе'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='покупатель'),
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='products',
            field=models.ManyToManyField(to='shopapp.products', verbose_name='Товары'),
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
