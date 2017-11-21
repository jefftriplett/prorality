from django import forms
from django.forms.widgets import TextInput, URLInput
from organizations.models import Organization

from . import models
from whatnots.forms import ContentManageableModelForm


class ProposalForm(ContentManageableModelForm):

    def __init__(self, request=None, organization_slug=None, *args, **kwargs):
        self.request = request
        self.organization_slug = organization_slug
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Proposal
        fields = (
            'subject',
            'body',
            'url',
            'closing_date',
        )
        widgets = {
            'subject': TextInput(),
            'url': URLInput(),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.organization = Organization.objects.get(slug=self.organization_slug)

        if commit:
            obj.save()
        return obj


# class VoteForm(ContentManageableModelForm):

#     class Meta:
#         model = models.Vote
#         fields = (
#             'proposal',
#             'user',
#             'vote',
#         )


class VoteForm(forms.Form):
    vote = forms.ChoiceField(widget=forms.RadioSelect, choices=models.Vote.VOTE_CHOICES)
    reason = forms.CharField(widget=forms.Textarea, required=False,
                             help_text='Required for +/-1 votes but optional for +/- 0 votes.')

    def __init__(self, request=None, organization_slug=None, *args, **kwargs):
        self.request = request
        self.organization_slug = organization_slug
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        vote = cleaned_data.get('vote')
        reason = cleaned_data.get('reason')
        if vote in [models.Vote.VOTE_PLUS_ONE, models.Vote.VOTE_MINUS_ONE] and len(reason) == 0:
            msg = 'Please state the reason why you are voting +/- 1'
            self.add_error('reason', msg)
