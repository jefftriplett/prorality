from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from . import models


class ProposalDetail(DetailView):
    slug_field = 'hashid'
    model = models.Proposal

    def get_object(self):
        return get_object_or_404(models.Proposal,
                                 organization__slug=self.kwargs.get('organization_slug'),
                                 hashid=self.kwargs.get('hashid'))


class ProposalList(ListView):
    model = models.Proposal

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(organization__slug=self.kwargs.get('organization_slug'))
        return queryset
