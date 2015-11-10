from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^list/$', views.ListView.as_view(), name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
]