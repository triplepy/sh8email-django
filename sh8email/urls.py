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
from sh8core import views as front_views
from sh8core import urls as front_urls
from rest import urls as rest_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^checkin/$', front_views.checkin, name='checkin'),
    url(r'', include(front_urls, namespace='front')),
    url(r'^rest/', include(rest_urls, namespace='rest')),
]
