from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Products


class ProductsForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:  
        model = Products
        fields = '__all__'


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']