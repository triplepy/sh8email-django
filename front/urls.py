from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^list/$', views.ListView.as_view(), name='list'),
]