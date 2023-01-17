from django.contrib import admin

from .models import Categories, Products, FeedbackModel

admin.site.register(Products)
admin.site.register(Categories)
admin.site.register(FeedbackModel)
