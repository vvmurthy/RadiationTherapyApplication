"""dsrt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^upload/',include('upload.urls')),
    url(r'^AlgoEngine/',include('AlgoEngine.urls')),
    url(r'^users/', include('UserProfile.urls')),

    url(r'^home/', views.home, name='home'),
    url(r'^about/', views.about, name='about'),
    url(r'^features/', views.features, name='features'),
    url(r'^faq/', views.faq, name='faq'),

    #keep the below url pattern at the very bottom
    url(r'^$', views.index, name='index'),
]
