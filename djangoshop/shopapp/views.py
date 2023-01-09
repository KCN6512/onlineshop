from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView, View, CreateView
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserRegistrationForm
from .models import Products

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

class UserRegistration(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


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



#TODO сделать обратную связь через форму, заказы,список заказов по дате и времени тесты 
