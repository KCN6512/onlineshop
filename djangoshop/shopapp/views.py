from django.views.generic import ListView
from django.shortcuts import render
from .models import Products

# Create your views here.

class HomeView(ListView):
    template_name = 'home.html'
    queryset = Products.objects.all()
    context_object_name = 'products'

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Домашняя страница магазина '
        return context


def product_view(request, code):
    return render(request, 'product.html', context={'code': code})

if __name__ == '__main__':
    import os
    command = 'py manage.py runserver'
    os.system(command)    
    