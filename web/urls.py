from django.conf.urls import url

from web import views

urlpatterns = [
    url(r'^$', views.intro, name='intro'),
    url(r'^list/$', views.list_, name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^help/$', views.help_, name='help'),
]
