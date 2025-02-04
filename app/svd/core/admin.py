"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models, forms
from famTree import forms as memberForm


class UserAdmin(BaseUserAdmin):
    """ Define the admin pages for users."""
    add_form = forms.svdUserAdminForm
    ordering = ["svdUser",]
    list_display = ["svdUser", "email"]
    fieldsets = (
        (None, {'fields': ('svdUser', 'email', 'password',)}),
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


class MemberAdmin(admin.ModelAdmin):
    """ Define the admin for members. """
    add_form = memberForm.MemberAdminForm
    ordering = ["birthday"]
    fieldsets = [
        (None, {'fields':
                ["lastname", "firstname", "call_name",
                 "sex", "birthday", "birthday_txt",
                 "father", "mother", "image"], }, ),
        (_("Administration"), {"fields":
                               ["editor", "note", "created", "modified",]}, )
    ]
    readonly_fields = ["editor", "created", "modified"]


admin.site.register(models.SvdUser, UserAdmin)
admin.site.register(models.Member, MemberAdmin)
