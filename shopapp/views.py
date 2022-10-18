from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):
    template_name: str = 'templates/home.html'




if __name__ == '__main__':
    import os
    command = 'py djangoshop/manage.py runserver'
    os.system(command)    
    