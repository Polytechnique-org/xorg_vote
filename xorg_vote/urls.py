# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

from django.urls import path
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
]
