from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from . import models
from whatnots.admin import ContentManageableAdmin


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
