from django.urls import path

from .views import HomeView, product_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:code>/', product_view, name='product')
]