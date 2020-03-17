# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render
from django.views import View, generic


class LoginView(generic.TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        ctxt = super(LoginView, self).get_context_data(**kwargs)
        next_url = ctxt.get('next') or self.request.GET.get('next') or settings.LOGIN_REDIRECT_URL
        ctxt.update({'next': next_url})
        return ctxt

class LogoutView(View):
    template_name = 'logout.html'

    def get(self, request):
        response = logout(request)
        return render(response, self.template_name)
