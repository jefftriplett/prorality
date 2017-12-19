from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View
from django.views.generic.edit import FormView

from . import forms
from . import models


class ProposalMixin(object):
    model = models.Proposal
    slug_field = 'pk'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organization_slug'] = self.kwargs.get('organization_slug')
        return context

    def get_object(self):
        return get_object_or_404(models.Proposal,
                                 organization__slug=self.kwargs.get('organization_slug'),
                                 pk=self.kwargs.get('pk'))


class ProposalCreate(LoginRequiredMixin, ProposalMixin, CreateView):
    form_class = forms.ProposalForm
    success_message = 'Proposal was created'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['organization_slug'] = self.kwargs.get('organization_slug')
        return kwargs


class ProposalDelete(LoginRequiredMixin, ProposalMixin, UserPassesTestMixin, DeleteView):
    success_message = 'Proposal was deleted'

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('proposals:proposal_list', kwargs={'organization_slug': self.kwargs.get('organization_slug')})

    def test_func(self):
        return True
        # return self.get_object() == self.request.user


class ProposalDetail(LoginRequiredMixin, ProposalMixin, DetailView):
    template_name = 'proposals/proposal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.VoteForm()
        return context


class ProposalList(LoginRequiredMixin, ProposalMixin, ListView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status', models.Proposal.STATUS_DRAFT)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(organization__slug=self.kwargs.get('organization_slug'))
        status = self.kwargs.get('status', models.Proposal.STATUS_DRAFT)
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class ProposalRawDetail(LoginRequiredMixin, ProposalMixin, DetailView):
    content_type = 'text/plain'
    template_name = 'proposals/proposal_raw_detail.html'


class ProposalUpdate(LoginRequiredMixin, ProposalMixin, UpdateView):
    form_class = forms.ProposalForm
    success_message = 'Proposal was updated'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_action'] = 'update'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['organization_slug'] = self.kwargs.get('organization_slug')
        return kwargs


class ChangeProposalStatus(LoginRequiredMixin, ProposalMixin, View):

    def get(self, request, organization_slug, pk):
        proposal = get_object_or_404(models.Proposal, organization__slug=organization_slug, pk=pk)
        proposal.status = self.new_status
        proposal.save()
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect('proposals:proposal_detail', organization_slug=organization_slug, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context


class ProposalDraft(ChangeProposalStatus):
    new_status = models.Proposal.STATUS_DRAFT
    success_message = 'Your proposal been re-drafted.'


class ProposalFinal(ChangeProposalStatus):
    new_status = models.Proposal.STATUS_FINAL
    success_message = 'Your proposal been published.'


class ProposalWithdrawn(ChangeProposalStatus):
    new_status = models.Proposal.STATUS_WITHDRAWN
    success_message = 'Your proposal been withdrawn.'


class VoteFormView(LoginRequiredMixin, ProposalMixin, FormView):
    form_class = forms.VoteForm
    success_message = 'Your vote has been recorded.'
    template_name = 'proposals/proposal_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['organization_slug'] = self.kwargs.get('organization_slug')
        return kwargs

    def form_valid(self, form):
        print(self.request.user.id)
        print(self.kwargs.get('organization_slug'))
        print(self.kwargs.get('pk'))
        print(form.cleaned_data['vote'])
        vote, created = models.Vote.objects.update_or_create(
            proposal__pk=self.kwargs.get('pk'),
            user=self.request.user.id,
            defaults={
                'vote': form.cleaned_data['vote'],
                'reason': form.cleaned_data.get('reason'),
            }
        )
        print(form.cleaned_data['vote'])
        return super(VoteFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('proposals:proposal_detail', kwargs={
            'organization_slug': self.kwargs.get('organization_slug'),
            'id': self.kwargs.get('id'),
        })
