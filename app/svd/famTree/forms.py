"""
Forms for member app.
"""

from django import forms
# from django.contrib.auth import get_user_model
from core.models import Member
from django.utils.translation import gettext_lazy as _


class MemberAdminForm(forms.ModelForm):
    """ Form for customizing member input in admin"""
    # print("I am in svdUserAdminForm")
    lastname = forms.CharField(max_length=63, help_text=_("Use your family name."))

    class Meta:
        model = Member
        fields = '__all__'

    def current_user(request):
        """ Returns the current user"""
        return request.user.id

    def save(self, commit=True):
        """ Save the member with editor in admin"""
        try:
            self.clean()
            print(f"In Save {self.cleaned_data}")
            self.cleaned_data["editor"] = self.current_user()
            member = super().save(commit)
        except KeyError:
            return False

        return member
