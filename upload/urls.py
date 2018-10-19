from django.conf.urls import url

from . import views

urlpatterns = [
	#ex: /users/
	url(r'^patients/$', views.view_patients, name='patients'),
	url(r'^patients/data/cts/$', views.scroll_cts, name='ct'),
	url(r'^patients/data/remove_ct/$', views.remove_ct, name='remove_ct'),
	
	# View patient / study / series CT scans
	url(r'^patients/data/(?P<slug>[-\w]+)/(?P<study_id>[-\w]+)/(?P<series_id>[-\w]+)/$', views.view_cts, name='view_cts'),

	# view studies for patient
	url(r'^patients/data/(?P<slug>[-\w]+)/$', views.view_studies, name='view_studies'),

	# view series for patient & study
	url(r'^patients/data/(?P<slug>[-\w]+)/(?P<study_id>[-\w]+)/$', views.view_series, name='view_series'),

	url(r'^$', views.uploadForm, name='upload'),

]
