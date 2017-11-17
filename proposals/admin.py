from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from . import models
from whatnots.admin import ContentManageableAdmin


@admin.register(models.Proposal)
class ProposalAdmin(ContentManageableAdmin, SimpleHistoryAdmin):
    list_display = [
        'subject',
        'created_by',
        'created',
    ]
    raw_id_fields = [
        'organization',
    ]
    readonly_fields = [
        'hashid',
    ]
