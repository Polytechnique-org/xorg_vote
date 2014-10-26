# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.decorators import login_required

import xorg_vote.votes.views
import xorg_vote.web.views


admin.autodiscover()
admin.site.login_template = 'authgroupex/admin_login.html'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^xorgauth/', include('django_authgroupex.urls', namespace='authgroupex')),
    url(r'^login/$', xorg_vote.web.views.LoginView.as_view(), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'},
        name='logout'),
    url(r'^403$', 'django.views.defaults.permission_denied'),
    url(r'^404$', 'django.views.defaults.page_not_found'),
    url(r'^500$', 'django.views.defaults.server_error'),
)

urlpatterns += patterns('',
    url(r'^$', login_required(xorg_vote.votes.views.IndexView.as_view()), name='index'),
    url(r'^(?P<pk>\d+)/$', login_required(xorg_vote.votes.views.DetailView.as_view()), name='detail'),
    url(r'^(?P<vote_id>\d+)/vote/$', login_required(xorg_vote.votes.views.vote), name='vote'),
    url(r'^(?P<pk>\d+)/ok/$', login_required(xorg_vote.votes.views.VoteOkView.as_view()), name='vote_ok'),
    url(r'^(?P<pk>\d+)/close/$', login_required(xorg_vote.votes.views.VoteCloseView.as_view()), name='vote_close'),
)
