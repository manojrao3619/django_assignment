from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(UserCreationForm):
    image = forms.ImageField(label='Your Picture')
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'placeholder': 'Fisrt Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Age'}))
    unique_id = forms.CharField(required = False, label='Unique Id', widget=forms.TextInput(attrs={'placeholder': 'Unique Id'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    
    class Meta:
        model = User
        exclude = ['username']
        fields = ['image','first_name', 'last_name', 'age', 'unique_id', 'email']

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email Id'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


        


