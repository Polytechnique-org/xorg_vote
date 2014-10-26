# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic

from xorg_vote.votes.models import Choice, Vote


class IndexView(generic.ListView):
    template_name = 'votes/index.html'
    context_object_name = 'votes_list'

    def get_queryset(self):
        votes_filter = Vote.objects.filter(pub_date__lte=timezone.now())
        # Filter out restricted votes for non-staff users
        if not self.request.user.is_staff:
            votes_filter = votes_filter.filter(restricted=False)
        votes = votes_filter.order_by('-pub_date')
        for v in votes:
            v.user_has_voted = v.has_voted(self.request.user)
        return votes


class DetailView(generic.DetailView):
    model = Vote
    template_name = 'votes/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        if self.object:
            context['user_has_voted'] = self.object.has_voted(self.request.user)
        return context


def results(request, vote_id):
    return HttpResponse("The results of vote %s are not yet implemented." % vote_id)


class VoteOkView(generic.DetailView):
    model = Vote
    template_name = 'votes/vote_ok.html'


class VoteView(generic.DetailView):
    model = Vote
    template_name = 'votes/detail.html'

    def post(self, request, *args, **kwargs):
        vote = get_object_or_404(Vote, pk=kwargs.get('pk'))

        # Deny non-staff users from voting to restricted votes
        if vote.restricted and not request.user.is_staff:
            raise PermissionDenied()

        # Check wether the user has already voted
        if vote.has_voted(request.user):
            messages.error(request, "Vous avez déjà voté.")
            return HttpResponseRedirect(reverse('detail', args=(vote.id,)))
        try:
            selected_choice = vote.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            messages.error(request, "Aucun choix n'a été sélectionné.")
            return HttpResponseRedirect(reverse('detail', args=(vote.id,)))
        else:
            selected_choice.user_votes.add(request.user)
            selected_choice.save()
            return HttpResponseRedirect(reverse('vote_ok', args=(vote.id,)))


class VoteCloseView(generic.DetailView):
    model = Vote
    template_name = 'votes/vote_close.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(VoteCloseView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        vote = get_object_or_404(Vote, pk=kwargs.get('pk'))
        vote.opened = False
        vote.save()
        return HttpResponseRedirect(reverse('detail', args=(vote.id,)))
