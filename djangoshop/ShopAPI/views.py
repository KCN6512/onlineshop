from django.db.models import *
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.permissions import *
from rest_framework.reverse import reverse
from shopapp.models import CartModel, OrderModel, Products
from .permissions import IsOwnerOrReadOnly
from .serializers import (CartSerializer, OrderSerializer,
                                 ProductsSerializer)


class ProductsViewSet(viewsets.ModelViewSet):
    '''Products viewset'''
    queryset = Products.objects.all().prefetch_related('categories')
    serializer_class = ProductsSerializer
    permission_classes = [DjangoModelPermissions]


class CartViewSet(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin):
    '''Cart viewset'''
    queryset = CartModel.objects.all().prefetch_related('products').select_related('user')
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class OrderViewSet(viewsets.GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin):
    '''Order viewset'''
    queryset = OrderModel.objects.all().prefetch_related('products').select_related('user')
    #  .prefetch_related(Prefetch('products', queryset=Products.objects.all().only('id')))
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
        #  redirect to created order
        return redirect(reverse('orders-detail', request=request,
                                            args=[response.data['id']]))

    @action(detail=False, methods=['get'])
    def recent_orders(self, request):
        return Response({'resent orders':OrderSerializer(self.queryset[:10],
                                                         many=True).data})
