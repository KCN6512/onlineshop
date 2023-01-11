from django.urls import path

from .views import (HomeView, LogoutView, ProductView, UserLoginView,
                    UserRegistrationView, BasketView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>/', ProductView.as_view(), name='product'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('basket/', BasketView.as_view(), name='basket')

]

handler404 = 'shopapp.views.page_not_found'