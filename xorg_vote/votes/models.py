# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.contrib.auth.models import User
from django.db import models


@python_2_unicode_compatible
class Vote(models.Model):
    shortdesc = models.CharField(max_length=500)
    shortdesc.short_description = 'Short description'
    description = models.TextField()
    pub_date = models.DateTimeField('date published')
    opened = models.BooleanField(default=True)
    restricted = models.BooleanField(default=True)
    restricted.verbose_name = 'Restreint au groupe'

    def __str__(self):
        return self.description

    def num_votes(self):
        return sum(c.num_votes() for c in self.choice_set.iterator())
    num_votes.short_description = 'Number of votes'

    def list_sorted_choices(self):
        choices = self.choice_set.all()
        return sorted(choices, key=lambda c: -c.num_votes())
    list_sorted_choices.short_description = 'List choices'

    def has_voted(self, user):
        """Return whether a user has already voted"""
        return user.choice_set.filter(vote=self).exists()


@python_2_unicode_compatible
class Choice(models.Model):
    vote = models.ForeignKey(Vote)
    text = models.CharField(max_length=500)
    user_votes = models.ManyToManyField(User)

    def __str__(self):
        return self.text

    def num_votes(self):
        return self.user_votes.count()

    def percent_votes(self):
        return 100. * float(self.user_votes.count()) / float(self.vote.num_votes())
