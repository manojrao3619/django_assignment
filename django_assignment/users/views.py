from django.shortcuts import render, redirect
from .forms import LoginForm, SignupForm
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse 
from .models import Profile
from django.contrib.auth.decorators import login_required
import secrets

def index_view(request):
	return render(request, 'index.html', {})

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			profile = Profile.objects.get(email=form.cleaned_data['email'])
			username = profile.user	
			password = form.cleaned_data['password']

			user = authenticate(username = username, password = password)
			if user is not None:
				rsp = requests.post('http://127.0.0.1:8000/api/token/'
					  , data={'username': username, 'password': password}).json()

				token = rsp['access']
				headers = {"Authorization":"Bearer " + token}
				rsp2 = requests.get('http://127.0.0.1:8000/auth/', headers=headers)

				if 'auth' in rsp2.text:
					js = rsp2.json()
					print(js['auth'])	
					login(request, user)
					return redirect(reverse('profile'))
				
				else:
					return render(request, 'login.html', {'form' : form, 'error': 'Something wrong ,try again'})
	      	
			else:
				return render(request, 'login.html', {'form' : form, 'error': 'Invalid Credentials'})

	else:
		form = LoginForm()

	return render(request, 'login.html', { 'form': form })

def signup_view(request):
	if request.method == 'POST':
		form = SignupForm(request.POST, request.FILES)
		if form.is_valid():
			username = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
			password = form.cleaned_data['password1']
			user = User.objects.create_user(username = username, password = password)
			user.profile.image = form.cleaned_data['image']
			user.profile.first_name = form.cleaned_data['first_name']
			user.profile.last_name  = form.cleaned_data['last_name']
			user.profile.age		= form.cleaned_data['age']

			if form.cleaned_data['unique_id'] == "":
				user.profile.unique_id	= secrets.token_hex(3)
			else:
				user.profile.unique_id	= form.cleaned_data['unique_id']

			user.profile.email = form.cleaned_data['email']
			user.save()
			form = SignupForm()
			return redirect(reverse('login'))
	else:
		form = SignupForm()
	return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
	profile = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		logout(request)
		return redirect(reverse('login'))
	return render(request, 'profile.html', {'profile': profile})
