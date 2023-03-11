from django.contrib import admin

from .models import *


models_list = [Products, Categories, FeedbackModel, CartModel, OrderModel,
               UserProfile]

admin.site.register(models_list)
