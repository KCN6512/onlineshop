from django.urls import path

from .views import HomeView, ProductView, UserRegistration

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>/', ProductView.as_view(), name='product'),
    path('register/', UserRegistration, name='registration'),
]

handler404 = 'shopapp.views.page_not_found'