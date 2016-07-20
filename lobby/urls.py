# coding: utf8
from django.conf.urls import patterns, include, url
from views import home, login, logout, register, room, privateroom
urlpatterns = [
    url(r'^$', home),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^register/$', register),
    url(r'^room/$', room),
    url(r'^room/(?P<sender_id>\d+)&(?P<receiver_id>\d+)/$', privateroom),
]