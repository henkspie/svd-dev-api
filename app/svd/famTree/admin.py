from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from famTree.models import Events, EventList, Location


class EventAdmin(admin.ModelAdmin):
    """ Define the admin pages for events."""
    ordering = ['member', 'date']
    list_display = ['member', 'date', 'event_type']
    verbose_name = _("Event")
    verbose_name_plural = ("Events")
    fieldsets = (
        (None, {'fields':
                ('member', 'event_type', 'date', 'end_date', 'source',)}),
        (_('Administration'), {
            'classes': ["collapse",],
            'fields': ['editor', 'created', 'modified',]
        },)
    )
    readonly_fields = ['editor', 'note', 'created', 'modified',]

    def save_model(self, request, obj, form, change):
        obj.editor = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(EventList)
admin.site.register(Location)
admin.site.register(Events, EventAdmin)
