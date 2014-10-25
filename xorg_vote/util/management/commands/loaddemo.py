# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

from django.core.management import base

from xorg_vote.votes import testing as vote_testing


class Command(base.NoArgsCommand):
    help = "Load a demo, standard database."

    def handle_noargs(self, **kwargs):
        for i in range(3):
            vote = vote_testing.ExampleVoteFactory.create()
            vote.shortdesc += " (closed)"
            vote.opened = False
            vote.save()
        for i in range(3):
            vote_testing.ExampleVoteFactory.create()
