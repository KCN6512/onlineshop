from django.urls import path

from .views import HomeView, Product_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>', Product_view.as_view(), name='product')
]
