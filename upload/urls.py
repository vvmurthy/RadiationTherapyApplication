from django.conf.urls import url

from . import views

urlpatterns = [
	#ex: /users/
	url(r'^patients/$', views.view_patients, name='patients'),
	
	# View patient / study / series CT scans
	url(r'^patients/data/(?P<slug>[-\w]+)/(?P<study_id>[-\w]+)/(?P<series_id>[-\w]+)/$', views.view_patient, name='view_patient'),

	# view studies for patient
	url(r'^patients/data/(?P<slug>[-\w]+)/$', views.view_studies, name='view_studies'),

	# view series for patient & study
	url(r'^patients/data/(?P<slug>[-\w]+)/(?P<study_id>[-\w]+)/$', views.view_series, name='view_series'),

	url(r'^$', views.uploadForm, name='upload'),

]
