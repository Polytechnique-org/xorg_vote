# -*- coding: utf-8 -*-
# Copyright (c) 2014 Polytechnique.org
# This software is distributed under the GPLv3+ license.

from django.contrib.auth.decorators import user_passes_test
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
        votes = Vote.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
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


def vote(request, vote_id):
    vote = get_object_or_404(Vote, pk=vote_id)
    if vote.has_voted(request.user):
        return render(request, 'xorg_vote/detail.html', {
            'vote': vote,
            'user_has_voted': True,
            'error_message': "Vous avez déjà voté.",
        })
    try:
        selected_choice = vote.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'votes/detail.html', {
            'vote': vote,
            'error_message': "Aucun choix n'a été sélectionné.",
        })
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
