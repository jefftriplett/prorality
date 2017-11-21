from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormView

from . import forms
from . import models


class ProposalMixin(object):
    model = models.Proposal
    slug_field = 'hashid'

    def get_object(self):
        return get_object_or_404(models.Proposal,
                                 organization__slug=self.kwargs.get('organization_slug'),
                                 hashid=self.kwargs.get('hashid'))


class ProposalCreate(LoginRequiredMixin, ProposalMixin, CreateView):
    form_class = forms.ProposalForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Proposal was created')
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['organization_slug'] = self.kwargs.get('organization_slug')
        return kwargs


class ProposalDelete(LoginRequiredMixin, ProposalMixin, UserPassesTestMixin, DeleteView):

    def get_success_url(self):
        return reverse('proposals:proposal_list', kwargs={'organization_slug': self.kwargs.get('organization_slug')})

    # def test_func(self):
    #     return self.get_object() == self.request.user


class ProposalDetail(LoginRequiredMixin, ProposalMixin, DetailView):
    template_name = 'proposals/proposal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.VoteForm()
        return context


class ProposalList(LoginRequiredMixin, ProposalMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_slug'] = self.kwargs.get('organization_slug', 'None')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(organization__slug=self.kwargs.get('organization_slug'))
        return queryset


class ProposalUpdate(LoginRequiredMixin, ProposalMixin, UpdateView):
    form_class = forms.ProposalForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Proposal was updated')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'update'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['organization_slug'] = self.kwargs.get('organization_slug')
        return kwargs


class ProposalVote(LoginRequiredMixin, ProposalMixin, DetailView):
    template_name = 'proposals/proposal_detail.html'


class VoteFormView(LoginRequiredMixin, FormView):
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
