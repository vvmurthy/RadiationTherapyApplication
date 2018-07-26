from django.conf.urls import url

from . import views

urlpatterns = [
	#ex: /users/
	url(r'^patients/$', views.view_patients, name='patients'),
	url(r'^patients/data/(?P<slug>[-\w]+)/$', views.view_patient, name='patient'),
	url(r'^$', views.uploadForm, name='upload'),

]
