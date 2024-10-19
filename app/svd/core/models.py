"""
Database models

"""
import datetime
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _


def check_normalize_svdUser(name):
    """Check the svdUser name construct is correct."""
    txt = name.split("_")
    if len(txt[1]) == 8 and txt[1].isnumeric():
        # we do not allow users older as 120 years or younger as 5
        year = int(txt[1][:4])
        now = int(datetime.datetime.now().year)
        # print(f"{txt[0]} {year} {now-120} {now-5}" )
        if year in range(now-120, now-5):
            return f"{txt[0].capitalize()}_{txt[1]}"

    return False


class SvdUserManager(BaseUserManager):
    """Manager fo SvdUsers."""

    def _create_user(self, svdUser, password, email, **extra_fields):
        """Create, save and return a new user."""
        svdUser = check_normalize_svdUser(svdUser)
        if not svdUser:
            raise ValueError(_("Not a correct SvdUser name given."))
        user = self.model(svdUser=svdUser, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, svdUser, password=None, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(svdUser, password, email, **extra_fields)

    def create_superuser(self, svdUser, password=None, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(svdUser, password, email, **extra_fields)


class SvdUser(AbstractBaseUser, PermissionsMixin):
    """ SvdUser in this system."""
    svdUser = models.CharField(_("Name_Birthday of the svdUser"), max_length=63, unique=True)
    email = models.EmailField(_("Email valid for the User of the this website"),
                              max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = SvdUserManager()
    USERNAME_FIELD = 'svdUser'
