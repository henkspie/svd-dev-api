"""
Forms for core app.
"""

from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from .models import SvdUser
from django.utils.translation import gettext_lazy as _


class svdUserAdminForm(BaseUserCreationForm):
    """ Form for customizing svdUser Admin login form"""
    # print("I am in svdUserAdminForm")
    birthday = forms.DateField(
        help_text=_("Please use the following format:<em><strong>YYYY-MM-DD</strong><em>."))
    name = forms.CharField(max_length=63,
                           help_text=_("Use your family name or one of your first names"))

    class Meta:
        model = SvdUser
        fields = '__all__'

    def clean_birthday(self):
        date = self.cleaned_data['birthday']
        date = str(date)
        date = date[:4]+date[5:7]+date[8:]
        return date

    def clean_name(self):
        name = self.cleaned_data.get("name")
        name = name.lower().capitalize()
        return name

    def clean_svdUser(self):
        birthday = self.cleaned_data['birthday']
        name = self.cleaned_data['name']
        return f"{name}_{birthday}"

    def save(self, commit=True):
        try:
            self.clean()
            self.cleaned_data['svdUser'] = self.clean_svdUser()
            # print(self.cleaned_data)
            user = super().save(commit=False)
            user.svdUser = self.cleaned_data.get('svdUser')
            new_user = super().save(commit)
        except KeyError:
            return False

        return new_user
