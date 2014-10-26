# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

import datetime 
from django.utils import timezone
import factory
import factory.django

from django.contrib.auth import models as auth_models
from . import models


class ExampleVoterFactory(factory.django.DjangoModelFactory):
    """User who has voted"""
    class Meta:
        model = auth_models.User

    username = factory.Sequence(lambda n: "john.demo%s" % n)
    first_name = "John"
    last_name = factory.Sequence(lambda n: "Demo%s" % n)


class ExampleChoiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Choice

    text = factory.Sequence(lambda n: "Choice #%s" % n)


class ExampleVoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Vote

    shortdesc = factory.Sequence(lambda n: "Vote #%s" % n)
    description = factory.Sequence(lambda n: "Description for vote #%s" % n)

    # The vote was published an hour ago
    pub_date = factory.LazyAttribute(
        lambda o: timezone.now() - datetime.timedelta(hours=1))
    opened = True
    restricted = factory.Sequence(lambda n: (n % 2) == 0)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        vote = model_class(*args, **kwargs)
        vote.save()
        for i in range(5):
            choice = ExampleChoiceFactory.create(vote=vote)
            for j in range(3):
                voter = ExampleVoterFactory.create()
                choice.user_votes.add(voter)
            vote.choice_set.add(choice)
        return vote
