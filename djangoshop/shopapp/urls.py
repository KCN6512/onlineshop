from django.urls import path

from .views import HomeView, Product_view, test

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:product_code>', Product_view.as_view(), name='product'),
    path('test', test)
]

handler404 = 'shopapp.views.page_not_found'