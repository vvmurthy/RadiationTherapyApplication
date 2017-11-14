from django.conf.urls import url

from . import views

urlpatterns = [
	#/users/
	url(r'^$', views.index, name='index'),
	
	#/users/login/
	url(r'^login/$', views.login, name='login'),

	#/users/signup/
	url(r'^signup/$', views.signup, name='signup'),
]
