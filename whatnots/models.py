from django.conf import settings
from django.db import models


class ContentManageable(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='created_%(class)s_set',
                                   null=True, blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='updated_%(class)s_set',
                                    null=True, blank=True)

    class Meta:
        abstract = True
