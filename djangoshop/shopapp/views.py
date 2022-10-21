from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Products
from .forms import ProductsForm

# Create your views here. py manage.py runserver

class HomeView(ListView):
    template_name = 'home.html'
    queryset = Products.objects.all()
    context_object_name = 'products'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Домашняя страница магазина'
        return context


class Product_view(DetailView):
    template_name = 'product.html'
    context_object_name = 'product'

    def get_object(self):
        return Products.objects.get(product_code=self.kwargs['product_code'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.get_object().name
        return context


def test(request):
    context = {}
    all_products = Products.objects.all()
    context['products'] = all_products
    context['output'] = ProductsForm(instance=Products.objects.get(pk=1))
    return render(request, 'test.html', context = context)

# def product_view(request, code):
#     product = Products.objects.get(product_code=code)
#     title = product.name
#     return render(request, 'product.html', context={'product': product, 'title': title})


    
#TODO сделать обратную связь через форму, заказы,список заказов по дате и времени 