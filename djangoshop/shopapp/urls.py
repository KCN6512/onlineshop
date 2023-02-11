from django.urls import path

from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>/', ProductView.as_view(), name='product'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('cart/', CartView.as_view(), name='cart',),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('remove_product/<int:product_code>/', remove_product_from_cart_view, name='remove_product'),
    path('add_product/<int:product_code>/', add_product_to_cart_view, name='add_product'),
    #path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/order/', OrderView.as_view(), name='order'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('thanks', ThanksView.as_view(), name='thanks'),

]

handler404 = 'shopapp.views.page_not_found'
