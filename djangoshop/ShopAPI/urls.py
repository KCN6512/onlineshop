from django.urls import include, path, re_path
from graphene_django.views import GraphQLView
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'carts', CartViewSet, basename='carts')
router.register(r'orders', OrderViewSet, basename='orders')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # RESTAPI
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # POST auth/login/
    path('api/v1/graphql', GraphQLView.as_view(graphiql=True)),
]
