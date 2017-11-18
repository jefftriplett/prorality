from django import forms

from . import models
from whatnots.forms import ContentManageableModelForm


class ProposalForm(ContentManageableModelForm):

    class Meta:
        model = models.Proposal
        fields = (
            'subject',
            'body',
            'url',
            'closing_date',
            'allow_comments',
        )


# class VoteForm(ContentManageableModelForm):

#     class Meta:
#         model = models.Vote
#         fields = (
#             'proposal',
#             'user',
#             'vote',
#         )


class VoteForm(forms.Form):
    vote = forms.ChoiceField(choices=models.VOTE_CHOICES)
