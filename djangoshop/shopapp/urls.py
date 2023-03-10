from django.urls import include, path, re_path
from rest_framework import routers

from .views import *
from ShopAPI.views import *
router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>/', ProductView.as_view(), name='product'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('cart/', CartView.as_view(), name='cart',),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('remove_product/<int:product_code>/', remove_product_from_cart_view, name='remove_product'),
    path('add_product/<int:product_code>/', add_product_to_cart_view, name='add_product'),
    path('cart/order/', OrderView.as_view(), name='order'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
    path('__debug__/', include('debug_toolbar.urls')), #DebugToolBar
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # RESTAPI
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),  #POST auth/login/

]

handler404 = 'shopapp.views.page_not_found'
