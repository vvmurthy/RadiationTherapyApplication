# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import ProfileForm
from .models import UserProfile

# Create your views here.

@login_required(login_url='/users/login/')
def options(request):
	profile = UserProfile.objects.get(user=request.user)
	if request.method == 'POST':
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			form.save(request.user)
	else:
		form = ProfileForm(None, initial=profile, instance=profile)

	return render(request, 'users/options.html', {'form':form})

#def login(request):
#	return render(request, 'users/login.html')

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			auth_login(request, user)
			return redirect('home')
	else:
		form = UserCreationForm()

	return render(request, 'users/signup/signup.html', {'form': form})
