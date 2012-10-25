from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from rulestats.core.models import *

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'rulestats.core.views.home', name='home'),
    
    url(r'^firewall/(?P<pk>\d+)/rules$', DetailView.as_view(queryset=Firewall.objects.select_related().all()),
        name='rules'),
)
