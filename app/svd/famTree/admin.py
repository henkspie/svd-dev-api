from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from famTree.models import Event, EventList


class EventAdmin(admin.ModelAdmin):
    """ Define the admin pages for events."""
    ordering = ['member', 'date']
    list_display = ['member', 'date', 'event_type']
    fieldsets = (
        (None, {'fields': ('member', 'date', 'event_type', 'place', 'note',)}),
        (_('Administration'), {
            'classes': ["collapse",],
            'fields': ['editor', 'created', 'modified',]
        },)
    )
    readonly_fields = ['editor', 'created', 'modified',]

    def save_model(self, request, obj, form, change):
        obj.editor = request.user
        return super().save_model(request, obj, form, change)


admin.site.register(EventList)
admin.site.register(Event, EventAdmin)
