from django.conf.urls import url
from django.contrib import admin

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	#/users/
	url(r'^$', views.index, name='index'),
	
	#/users/login/
	url(r'^login/$', auth_views.login, {'template_name': 'users/login/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),

	#/users/signup/
	url(r'^signup/$', views.signup, name='signup'),
]
