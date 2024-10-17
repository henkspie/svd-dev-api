"""
Database models

"""
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


class SvdUserManager(BaseUserManager):
    """Manager fo SvdUsers."""

    def create_user(self, svdUser, password=None, **extra_fields):
        """Create, save and return a new user."""
        user = self.model(svdUser=svdUser, email=None, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class SvdUser(AbstractBaseUser, PermissionsMixin):
    """ SvdUser in this system."""
    svdUser = models.CharField(_("Name_Birthday of the svdUser"), max_length=63, unique=True)
    email = models.EmailField(_("Email valid for the User of the this website"),
                              max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = SvdUserManager()
    USERNAME_FIELD = 'svdUser'