from django.conf import settings
from django.db import models
from simple_history.models import HistoricalRecords

from whatnots.models import ContentManageable


VOTE_CHOICES = (
    (0, "+1: Yes, I agree"),
    (1, "+0: I don't feel strongly about it, but I'm okay with this."),
    (2, "-0: I won't get in the way, but I'd rather we didn't do this."),
    (3, "-1: I object on the following grounds"),
)


class Vote(ContentManageable):
    proposal = models.ForeignKey('proposals.Proposal', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    vote = models.IntegerField(choices=VOTE_CHOICES)

    history = HistoricalRecords()

    class Meta:
        unique_together = (
            ('proposal', 'user'),
        )

    def __str__(self):
        return '{vote} from {proposal} on {proposal}'.format(
            vote=self.get_vote_display(),
            token=self.proposal.subject,
            proposal=self.proposal)
