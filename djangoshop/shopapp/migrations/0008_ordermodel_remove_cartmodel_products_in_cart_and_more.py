# Generated by Django 4.1.2 on 2023-02-02 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopapp', '0007_alter_feedbackmodel_options_alter_products_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.PositiveIntegerField(null=True, unique=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('price_sum', models.IntegerField()),
                ('products', models.ManyToManyField(to='shopapp.products')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.RemoveField(
            model_name='cartmodel',
            name='products_in_cart',
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='products',
            field=models.ManyToManyField(to='shopapp.products', verbose_name='Товары'),
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders', models.ManyToManyField(related_name='orders', to='shopapp.ordermodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]