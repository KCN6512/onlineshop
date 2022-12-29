from django.urls import path

from .views import HomeView, ProductView, test, Test2

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>', ProductView.as_view(), name='product'),
    path('test', test),
    path('test2', Test2.as_view())
]

handler404 = 'shopapp.views.page_not_found'