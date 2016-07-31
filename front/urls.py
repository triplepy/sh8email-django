from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.intro, name='intro'),
    url(r'^wehavesecret', views.wehavesecret, name='wehavesecret'),
    url(r'^list/$', views.list_, name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^help/$', views.help_, name='help'),
]