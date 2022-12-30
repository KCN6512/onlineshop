from django import forms

from .models import Products
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductsForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:  
        model = Products
        fields = '__all__'

class UserRegistrationForm(UserCreationForm):

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")