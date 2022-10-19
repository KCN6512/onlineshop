from django.shortcuts import render
from django.views.generic import ListView

from .models import Products

# Create your views here. py manage.py runserver

class HomeView(ListView):
    template_name = 'home.html'
    queryset = Products.objects.all()
    context_object_name = 'products'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Домашняя страница магазина'
        return context


def product_view(request, code):
    product = Products.objects.get(product_code=code)
    title = product.name
    return render(request, 'product.html', context={'product': product, 'title': title})


    
#TODO сделать обратную связь через форму, заказы,список заказов по дате и времени 