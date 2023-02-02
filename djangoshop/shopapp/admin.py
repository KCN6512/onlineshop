from django.contrib import admin

from .models import *

admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(FeedbackModel)
admin.site.register(CartModel)
admin.site.register(OrderModel)
admin.site.register(UserProfile)
