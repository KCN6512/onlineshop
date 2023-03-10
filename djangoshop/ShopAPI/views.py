from rest_framework import viewsets
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.permissions import *
from djangoshop.shopapp.models import CartModel, OrderModel, Products
from djangoshop.shopapp.permissions import IsOwnerOrReadOnly
from djangoshop.shopapp.serializers import CartSerializer, OrderSerializer, ProductsSerializer
from django.db.models import *
from django.http import HttpResponseRedirect



class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all().prefetch_related('categories')
    serializer_class = ProductsSerializer
    permission_classes = [DjangoModelPermissions]


class CartViewSet(viewsets.GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin):
    queryset = CartModel.objects.all().prefetch_related('products').select_related('user')
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    queryset = OrderModel.objects.all().prefetch_related('products').select_related('user')
    #.prefetch_related(Prefetch('products', queryset=Products.objects.all().only('id')))
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        response = super().list(request, *args, **kwargs)
        response_data = {'result': response.data}
        response_data['total_amount'] = queryset.aggregate(total=Sum('total_price'))
        response.data = response_data
        return response

    def perform_create(self, serializer):
        serializer = serializer.save(user=self.request.user, total_price=0)
        serializer.total_price = serializer.products.all().aggregate(
                                 Sum('price')).get('price__sum')
        return super().perform_create(serializer)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return HttpResponseRedirect(str(response.data['id']))