"""sh8email URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from rest import urls as rest_urls
from web import urls as web_urls
from web import views as web_views
from sh8core import views as core_views


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^checkin/$', web_views.checkin, name='checkin'),
    url(r'', include(web_urls, namespace='web')),
    url(r'^rest/', include(rest_urls, namespace='rest')),
    url(r'^create-dummies/$', core_views.create_dummies, name='create_dummies')
]
