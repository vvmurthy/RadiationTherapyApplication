# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, 'users/options.html')

def login(request):
	return render(request, 'users/login/login.html')

def signup(request):
	return render(request, 'users/signup/signup.html')
