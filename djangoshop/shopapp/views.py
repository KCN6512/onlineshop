from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, FeedbackForm
from .models import FeedbackModel, Products, CartModel, OrderModel, UserProfile


class HomeView(ListView):
    template_name = 'home.html'
    queryset = Products.objects.all()
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Домашняя страница магазина'
        return context


class ProductView(DetailView):
    template_name = 'product.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Products,product_code=self.kwargs['product_code'])

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_object().name
        return context


class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login') #reverse_lazy нужен для классов вьюшек

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


class CartView(LoginRequiredMixin, ListView):
    template_name = 'cart.html'
    context_object_name = 'cart'

    def get_queryset(self):
        queryset = CartModel.objects.get(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'

        if self.get_queryset().products.exists():
            context['total_price'] = self.get_queryset().price_summary()

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


class OrderView(View):
    success_url = reverse_lazy('thanks')#TODO сделать thanks.html

    def get(self, request, *args, **kwargs):
        return render(request, 'order.html')

    def post(self, request, *args, **kwargs):
        try:
            order = OrderModel()#TODO попробовать убрать лишний save
            order.save()
            products = CartModel.objects.get(user=request.user).products.all()
            order.products.set(products)
            order.user = request.user
            order.save()
            profile = UserProfile.objects.get(user=self.request.user)
            profile.orders.add(order)
        except:
            HttpResponse('Произошла ошибка, попробуйте попоже')
        finally:
            cart = CartModel.objects.get(user=request.user)
            items_to_remove = [i for i in cart.products.all()]
            cart.products.remove(*items_to_remove)

        return HttpResponseRedirect(reverse_lazy('home'))#TODO сменить на благодарность

class ProfileView(TemplateView):
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = 'Order'
        return context

def page_not_found(request, exception):
    return render(request, '404.html')

# TODO заказы,
# список заказов по дате в профиле и времени тесты , перенести на postgre и сделать docker
# потом drf requirements  debug toolbar  профиль пользователя

# в корзине товары добавляются к заказу и переход на старницу заказа где заказ оформляется
# отзывы
