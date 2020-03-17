# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

from django.conf import settings
from django.urls import include, path

from django.contrib import admin
from django.contrib.auth.decorators import login_required

import xorg_vote.votes.views
import xorg_vote.web.views


admin.autodiscover()
# admin.site.login_template = 'authgroupex/admin_login.html'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oidc/', include('mozilla_django_oidc.urls')),

    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', xorg_vote.web.views.LoginView.as_view(), name='login'),
    # path('logout/', 'django.contrib.auth.logout', {'template_name': 'logout.html'}, name='logout'), # FIXME
    # path('403', 'django.views.defaults.permission_denied'),
    # path('404', 'django.views.defaults.page_not_found'),
    # path('500', 'django.views.defaults.server_error'),

    path('', login_required(xorg_vote.votes.views.IndexView.as_view()), name='index'),
    path('<int:pk>/', login_required(xorg_vote.votes.views.DetailView.as_view()), name='detail'),
    path('<int:pk>vote/', login_required(xorg_vote.votes.views.VoteView.as_view()), name='vote'),
    path('<int:pk>/ok/', login_required(xorg_vote.votes.views.VoteOkView.as_view()), name='vote_ok'),
    path('<int:pk>/close/', login_required(xorg_vote.votes.views.VoteCloseView.as_view()), name='vote_close'),
]
