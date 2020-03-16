# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Vote(models.Model):
    shortdesc = models.CharField(max_length=500)
    shortdesc.verbose_name = "Nom du vote"
    description = models.TextField()
    pub_date = models.DateTimeField('date published')
    pub_date.verbose_name = "Date d'ouverture"
    opened = models.BooleanField(default=True)
    opened.verbose_name = "Ouvert"
    restricted = models.BooleanField(default=True)
    restricted.verbose_name = "Restreint au groupe"

    def __str__(self):
        return self.shortdesc

    def num_votes(self):
        return sum(c.num_votes() for c in self.choice_set.iterator())
    num_votes.short_description = "Nombre de votes"

    def list_sorted_choices(self):
        choices = self.choice_set.all()
        return sorted(choices, key=lambda c: -c.num_votes())

    def has_voted(self, user):
        """Return whether a user has already voted"""
        return user.choice_set.filter(vote=self).exists()


class Choice(models.Model):
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    text.verbose_name = "Texte"
    user_votes = models.ManyToManyField(User)

    def __str__(self):
        return self.text

    def num_votes(self):
        return self.user_votes.count()

    def percent_votes(self):
        num_votes = self.vote.num_votes()
        if num_votes == 0:
            return 0.
        return 100. * float(self.user_votes.count()) / float(num_votes)
