from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property
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

    STATUS_DRAFT = 'draft'
    STATUS_FINAL = 'final'
    STATUS_WITHDRAWN = 'withdrawn'
    STATUS_ACCEPTED = 'accepted'
    STATUS_REJECTED = 'rejected'
    STATUS_SUPERSEDED = 'superseded'
    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_FINAL, 'Final'),
        (STATUS_WITHDRAWN, 'Withdrawn'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
        # (STATUS_SUPERSEDED, 'Superseded'),
    ]
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    history = HistoricalRecords(excluded_fields=['_body_rendered', 'body_markup_type'])

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('proposals:proposal_detail', kwargs={
            'organization_slug': self.organization.slug,
            'hashid': self.hashid,
        })

    def get_accepting_votes(self):
        return self.status in [self.STATUS_DRAFT, self.STATUS_FINAL]

    def get_proposal_vote_form_url(self):
        return reverse('proposals:proposal_vote_form', kwargs={
            'organization_slug': self.organization.slug,
            'hashid': self.hashid,
        })

    def get_hashid(self):
        hashids = Hashids(salt=settings.HASHID_SALT, min_length=settings.HASHID_MIN_LENGTH)
        return hashids.encode(self.id)

    @cached_property
    def positive_votes(self):
        votes = Vote.objects.filter(proposal=self, vote=Vote.VOTE_PLUS_ONE).count()
        return votes

    @cached_property
    def neutral_votes(self):
        votes = Vote.objects.filter(proposal=self, vote__in=[Vote.VOTE_PLUS_ZERO, Vote.VOTE_MINUS_ZERO]).count()
        return votes

    @cached_property
    def negative_votes(self):
        votes = Vote.objects.filter(proposal=self, vote=Vote.VOTE_MINUS_ONE).count()
        return votes

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        if not self.hashid:
            self.hashid = self.get_hashid()
            self.save()
        return obj


class Vote(ContentManageable):
    proposal = models.ForeignKey('proposals.Proposal', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    VOTE_PLUS_ONE = 'plus_one'
    VOTE_PLUS_ZERO = 'plus_zero'
    VOTE_MINUS_ZERO = 'minus_zero'
    VOTE_MINUS_ONE = 'minus_one'
    VOTE_CHOICES = (
        (VOTE_PLUS_ONE, "+1: Yes, I agree"),
        (VOTE_PLUS_ZERO, "+0: I don't feel strongly about it, but I'm okay with this."),
        (VOTE_MINUS_ZERO, "-0: I won't get in the way, but I'd rather we didn't do this."),
        (VOTE_MINUS_ONE, "-1: I object on the following grounds"),
    )
    vote = models.CharField(max_length=16, choices=VOTE_CHOICES, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)

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
