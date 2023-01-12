from django.urls import path

from .views import (HomeView, LogoutView, ProductView, UserLoginView,
                    UserRegistrationView, CartView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>/', ProductView.as_view(), name='product'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cart/', CartView.as_view(), name='cart')

]

handler404 = 'shopapp.views.page_not_found'