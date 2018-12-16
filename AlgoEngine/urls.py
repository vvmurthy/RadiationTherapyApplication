from django.conf.urls import url

from . import views

urlpatterns = [
	
	# Query the CT of a given frame
	url(r'^ct_images/(?P<patient_id>[-\w]+)/(?P<study_id>[-\w]+)/(?P<series_id>[-\w]+)/(?P<roi_index>[-\w]+)/(?P<index>[-\w]+)/(?P<checked>\w+)/$', views.update_ct, name='update'),
	url(r'^ct_images/(?P<patient_id>[-\w]+)/(?P<study_id>[-\w]+)/(?P<series_id>[-\w]+)/$', views.get_ct, name='view_cts'),

	# Get the plan data
	url(r'^plan/(?P<patient_id>[-\w]+)/(?P<study_id>[-\w]+)/(?P<series_id>[-\w]+)/$', views.get_ct, name='view_cts'),

]
