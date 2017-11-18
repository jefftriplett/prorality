from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from . import forms
from . import models


class ProposalDetail(DetailView):
    slug_field = 'hashid'
    model = models.Proposal
    template_name = 'proposals/proposal_detail.html'

    def get_object(self):
        return get_object_or_404(models.Proposal,
                                 organization__slug=self.kwargs.get('organization_slug'),
                                 hashid=self.kwargs.get('hashid'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.VoteForm()
        return context


class ProposalList(ListView):
    model = models.Proposal

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(organization__slug=self.kwargs.get('organization_slug'))
        return queryset


class ProposalVote(DetailView):
    slug_field = 'hashid'
    model = models.Proposal
    template_name = 'proposals/proposal_detail.html'

    def get_object(self):
        return get_object_or_404(models.Proposal,
                                 organization__slug=self.kwargs.get('organization_slug'),
                                 hashid=self.kwargs.get('hashid'))


class VoteFormView(FormView):
    form_class = forms.VoteForm
    success_url = '/thanks/'
    template_name = 'proposals/proposal_detail.html'

    def form_valid(self, form):
        print(self.request.user.id)
        print(self.kwargs.get('organization_slug'))
        print(self.kwargs.get('hashid'))
        print(form.cleaned_data['vote'])
        return super(VoteFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('proposals:proposal_detail', kwargs={
            'organization_slug': self.kwargs.get('organization_slug'),
            'hashid': self.kwargs.get('hashid'),
        })
