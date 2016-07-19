# coding: utf8
from django.conf.urls import patterns, include, url
from views import *
urlpatterns = [
    url(r'^$', home),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^register/$', register),
    url(r'^room/$', room)
]