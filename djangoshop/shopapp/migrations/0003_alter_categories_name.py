# Generated by Django 4.1.2 on 2023-03-02 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0002_alter_ordermodel_options_ordermodel_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Название категории'),
        ),
    ]
