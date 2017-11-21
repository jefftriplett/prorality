from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from hashids import Hashids
from markupfield.fields import MarkupField
from simple_history.models import HistoricalRecords

from organizations.models import Organization
from whatnots.models import ContentManageable


DEFAULT_MARKUP_TYPE = getattr(settings, 'DEFAULT_MARKUP_TYPE', 'markdown')


class Proposal(ContentManageable):
    hashid = models.CharField(max_length=16, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    subject = models.TextField()
    body = MarkupField(default_markup_type=DEFAULT_MARKUP_TYPE,
                       null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    allow_comments = models.BooleanField(default=False)

    STATUS_DRAFT = 1
    STATUS_FINAL = 2
    STATUS_ACCEPTED = 3
    STATUS_REJECTED = 4
    STATUS_SUPERSEDED = 5
    STATUS_WITHDRAWN = 6
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_FINAL, 'Final'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        # (STATUS_SUPERSEDED, 'Superseded'),
        (STATUS_WITHDRAWN, 'Withdrawn'),
    ]
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=STATUS_DRAFT)

    history = HistoricalRecords(excluded_fields=['_body_rendered', 'body_markup_type'])

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('proposals:proposal_detail', kwargs={
            'organization_slug': self.organization.slug,
            'hashid': self.hashid,
        })

    def get_proposal_vote_form_url(self):
        return reverse('proposals:proposal_vote_form', kwargs={
            'organization_slug': self.organization.slug,
            'hashid': self.hashid,
        })

    def get_hashid(self):
        hashids = Hashids(salt=settings.HASHID_SALT, min_length=settings.HASHID_MIN_LENGTH)
        return hashids.encode(self.id)

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        if not self.hashid:
            self.hashid = self.get_hashid()
            self.save()
        return obj


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
