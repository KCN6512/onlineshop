from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View

from .forms import UserLoginForm, UserRegistrationForm
from .models import Categories, Products

# Create your views here.

class HomeView(ListView):
    template_name = 'home.html'
    queryset = Products.objects.all()
    context_object_name = 'products'

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

class UserRegistration(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='register.html',
        context={'register_form': UserRegistrationForm, 'title': 'Регистрация'})

    def post(self, request, *args, **kwargs):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request=request, template_name='register.html', context={'register_form': form,
        'title': 'Регистрация'})


class UserLogin(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='login.html', context={'form': UserLoginForm,
        'title': 'Вход'})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            return render(request=request, template_name='login.html',
            context={'form': UserLoginForm, 'title': 'Вход'})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        return render(request=request, template_name='logout.html')

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


def page_not_found(request, exception):
    return render(request, '404.html')



#TODO сделать обратную связь через форму, заказы,список заказов по дате и времени 
