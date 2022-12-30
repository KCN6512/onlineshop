from django.contrib.auth import login
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from django.contrib.auth.views import LoginView

from .forms import UserRegistrationForm
from .models import Products

# Create your views here.

class HomeView(ListView):
    template_name = 'home.html'
    queryset = Products.objects.all()
    context_object_name = 'products'

    def get(self, request):
        print(Products.objects.filter(name='Xbox Series X').aggregate(Sum('price')))
        #print(request.META['CONTENT_TYPE'])
        #print(request.headers['Header_name'])
        print(request.GET) #get параметры
        return super().get(request)

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


def UserRegistration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request=request, template_name='register.html', context={'register_form': form})
    else:
        return render(request=request, template_name='register.html', context={'register_form': UserRegistrationForm})

class Login(LoginView):
    pass
#TODO переделать в классы
def page_not_found(request, exception):
    return render(request, '404.html')

# def product_view(request, code):
#     product = Products.objects.get(product_code=code)
#     title = product.name
#     return render(request, 'product.html', context={'product': product, 'title': title})


#TODO сделать обратную связь через форму, заказы,список заказов по дате и времени 
