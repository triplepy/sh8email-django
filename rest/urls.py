from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^mail/list/$', views.MailList.as_view(), name='rest-mail-list'),
    url(r'^mail/(?P<pk>[0-9]+)/$', views.MailDetail.as_view(), name='rest-mail-detail'),
]