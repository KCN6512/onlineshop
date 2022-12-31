from django.urls import path

from .views import HomeView, ProductView, UserRegistration, UserLogin, LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>/', ProductView.as_view(), name='product'),
    path('register/', UserRegistration.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]

handler404 = 'shopapp.views.page_not_found'