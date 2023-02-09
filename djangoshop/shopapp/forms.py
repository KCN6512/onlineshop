from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import *


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = '__all__'
