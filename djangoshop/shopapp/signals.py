from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import UserProfile, CartModel

#при регистрации пользователя создает ему корзину и профиль с заказами
@receiver(post_save, sender=User)
def create_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        cart = CartModel.objects.create(user=instance)
        UserProfile.objects.create(user=instance, cart=cart)
