class ContentManageableAdmin(object):

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        return fields + [
            'created',
            'created_by',
            'modified',
            'modified_by',
        ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        else:
            obj.modified_by = request.user

        return super().save_model(request, obj, form, change)
