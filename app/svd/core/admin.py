"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models, forms


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users."""
    add_form = forms.svdUserAdminForm
    ordering = ["svdUser",]
    list_display = ["svdUser", "email"]
    fieldsets = (
        (None, {'fields': ('svdUser', 'email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ['last_login', ]}),
    )
    readonly_fields = ['last_login', "svdUser"]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                # 'svdUser',
                'birthday',
                'name',
                'email',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

    def name(self, admin):
        name = admin.svdUser.split('_')[0]
        return f"{name}"

    def birthday(self, admin):
        try:
            birthday = admin.svdUser.split('_')[1]
            return f"{birthday[:4]}-{birthday[4:6]}-{birthday[6:8]}"
        except:     # noqa :E722
            return _("No Date")


admin.site.register(models.SvdUser, UserAdmin)
