from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^mail/(?P<nickname>\w+)/list/$', views.MailList.as_view(), name='rest-mail-list'),
    url(r'^mail/(?P<nickname>\w+)/(?P<pk>[0-9]+)/$', views.MailDetail.as_view(), name='rest-mail-detail'),
]
