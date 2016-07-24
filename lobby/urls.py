# coding: utf8
from django.conf.urls import url
from views import home, login, logout, register, room
urlpatterns = [
    url(r'^$', home),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^register/$', register),
    url(r'^room/(?P<receiver_id>\d+)/$', room),
]