from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from . import models
from whatnots.admin import ContentManageableAdmin


@admin.register(models.Proposal)
class ProposalAdmin(ContentManageableAdmin, SimpleHistoryAdmin):
    list_display = [
        'subject',
        'status',
        'organization',
        'allow_comments',
        'created_by',
        'created',
    ]
    list_filter = [
        'status',
        'allow_comments',
    ]
    raw_id_fields = [
        'organization',
    ]
    readonly_fields = [
        'hashid',
    ]


@admin.register(models.Vote)
class VoteAdmin(ContentManageableAdmin, SimpleHistoryAdmin):
    list_display = [
        '__str__',
        'created_by',
        'created',
    ]
    raw_id_fields = [
        'proposal',
        'user',
    ]
