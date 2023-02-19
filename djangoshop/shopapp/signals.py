from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import *


# При регистрации пользователя создает ему корзину и профиль с заказами
@receiver(post_save, sender=User)
def create_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        cart = CartModel.objects.create(user=instance)
        UserProfile.objects.create(user=instance, cart=cart)

# Добавление заказа в профиль
@receiver(post_save, sender=OrderModel)
def add_order_to_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.get(user=instance.user)
        profile.orders.add(instance)