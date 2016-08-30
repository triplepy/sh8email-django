from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list/$', views.MailList.as_view(), name='rest-mail-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.MailList.as_view(), name='rest-mail-detail'),
]