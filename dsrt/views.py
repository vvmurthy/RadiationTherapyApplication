from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse

#Create your views here.

def index(request):
	return render(request, 'dsrt/home.html')

def home(request):
	return render(request, 'dsrt/home.html')

def about(request):
	return render(request, 'dsrt/about.html')

def features(request):
	return render(request, 'dsrt/features.html')

def faq(request):
	return render(request, 'dsrt/faq.html')


