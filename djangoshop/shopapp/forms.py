from django import forms

from .models import Products


class ProductsForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    product_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    price = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:  
        model = Products
        fields = '__all__'