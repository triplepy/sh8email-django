from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^raise_error/$', views.raise_error, name='raise_error'),
]