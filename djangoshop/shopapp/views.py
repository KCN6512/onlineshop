from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, View
from rest_framework import viewsets
from rest_framework.generics import *
from rest_framework.mixins import *
from rest_framework.permissions import *

from .forms import FeedbackForm, UserRegistrationForm
from .models import *
from .permissions import *
from .serializers import *


class HomeView(ListView):
    template_name = 'home.html'
    queryset = Products.objects.all().prefetch_related('categories')
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Домашняя страница магазина'
        return context


class ProductView(TemplateView):
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = get_object_or_404(Products,product_code=self.kwargs['product_code'])
        context['title'] = context['product'].name
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login_view') #reverse_lazy нужен для классов вьюшек

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class UserLoginView(LoginView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('home')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart.html'
    login_url = reverse_lazy('login_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = CartModel.objects.get(user=self.request.user)
        context['title'] = 'Корзина'

        if cart.products.exists():
            context['products'] = cart.products.all()
            context['total_price'] = cart.price_summary()
        return context


def remove_product_from_cart_view(request, product_code):
    product = get_object_or_404(Products, product_code=product_code)
    cart = get_object_or_404(CartModel, user=request.user)
    cart.products.remove(product)
    return HttpResponseRedirect(reverse_lazy('cart'))


def add_product_to_cart_view(request, product_code):
    product = get_object_or_404(Products, product_code=product_code)
    cart = get_object_or_404(CartModel, user=request.user)
    cart.products.add(product)
    return HttpResponseRedirect(reverse_lazy('cart'))


class FeedbackView(CreateView):
    form_class = FeedbackForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Обратная связь'
        return context


class OrderView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_view')

    def get(self, request, *args, **kwargs):
        cart = CartModel.objects.get(user=request.user)
        price = cart.price_summary() if cart.price_summary() else None
        context = {'price': price}
        context['title'] = 'Заказ'

        if not cart.products.exists():
            return HttpResponse('<h1>Корзина пуста, заказ невозможен</h1>')
        return render(request, 'order.html', context=context)

    def post(self, request, *args, **kwargs):
        try:
            cart = CartModel.objects.prefetch_related('products').get(user=request.user)
            products = cart.products.all()
            order = OrderModel(user=request.user, total_price=0)
            order.save()
            order.products.set(products)
            if not order.products.exists():
                return HttpResponse('<h1>Заказ пуст, продолжение невозможно</h1>')
            order.total_price=order.price_summary()
            order.save()
            # Удаление купленных товаров из корзины
            items_to_remove = [i for i in cart.products.all()]
            cart.products.remove(*items_to_remove)
        except:
            return HttpResponse('''<h1>Произошла ошибка, попробуйте позже
            или свяжитесь с нами через форму обратной связи</h1>''')
        return HttpResponseRedirect(reverse_lazy('thanks'))


class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login_view')
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = UserProfile.objects.get(user=self.request.user)
        context['orders'] = profile.orders.all().prefetch_related('products')
        context['title'] = 'Профиль'
        return context


class ThanksView(TemplateView):
    template_name = 'thanks.html'


# rest framework
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
                                 models.Sum('price')).get('price__sum')
        return super().perform_create(serializer)

def page_not_found(request, exception):
    return render(request, '404.html')


# TODO
# тесты code coverage %
# кешировать заказы
# pep8 linter
# git actions тесты