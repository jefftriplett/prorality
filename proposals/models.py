from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from hashids import Hashids
from markupfield.fields import MarkupField
from simple_history.models import HistoricalRecords

from organizations.models import Organization
from whatnots.models import ContentManageable


DEFAULT_MARKUP_TYPE = getattr(settings, 'DEFAULT_MARKUP_TYPE', 'markdown')

PROPOSAL_CHOICES = [
    ('', ''),
    ('', ''),
    ('', ''),
]


class Proposal(ContentManageable):
    hashid = models.CharField(max_length=16, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    subject = models.TextField()
    body = MarkupField(default_markup_type=DEFAULT_MARKUP_TYPE,
                       null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)

    history = HistoricalRecords(excluded_fields=['_body_rendered', 'body_markup_type'])

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('proposals:proposal_detail', kwargs={
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
