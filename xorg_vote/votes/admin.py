# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

from django.contrib import admin
from xorg_vote.votes.models import Choice, Vote


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3
    fields = ['text']


class VoteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['shortdesc', 'description', 'opened']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('shortdesc', 'pub_date', 'num_votes', 'opened')


admin.site.register(Vote, VoteAdmin)
