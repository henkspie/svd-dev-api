"""
Database models

"""
import datetime
import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _

from .abstract_models import StampedBaseModel


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

    raise NameError(_("Not a correct svdUser name given."))


def check_svdUser_in_members(name):
    """ Check if svdUser is in the members db"""
    # only members can create an account
    name = name.split("_")
    bd = name[1]
    bd = f"{bd[:4]}-{bd[4:6]}-{bd[6:]}"
    # print(bd)
    candidates = Member.objects.filter(birthday=bd).values()
    if candidates:
        for name in candidates:
            print(candidates.lastname)
        else:
            print("No candidates")

    raise ValueError(_("You are not in the db"))


class SvdUserManager(BaseUserManager):
    """Manager fo SvdUsers."""

    def _create_user(self, name, birthday, password, email, **extra_fields):
        """Create, save and return a new user."""
        # If name is given than the new user is requested by HTML.
        # Tests and admin will not be checked on existence in member.
        # Tests if 'example.com' is included in the email address.
        # admin will not use this routine.
        if name:
            date = str(birthday)
            date = date[:4]+date[5:7]+date[8:]
            user = f"{name}_{date}"
            if "example.com" not in email:
                user = check_svdUser_in_members(user)
        else:
            user = extra_fields["svdUser"]

        extra_fields["svdUser"] = check_normalize_svdUser(user)

        try:
            new_user = self.model(email=self.normalize_email(email), **extra_fields)
            new_user.set_password(password)
            new_user.save(using=self._db)
        except Exception:
            raise ValueError("Save Error")
        return new_user

    def create_user(self, name=None, birthday=None,
                    password=None, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, birthday, password, email, **extra_fields)

    def create_superuser(self, name=None, birthday=None,
                         password=None, email=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(name, birthday, password, email, **extra_fields)


class SvdUser(AbstractBaseUser, PermissionsMixin):
    """ SvdUser in this system."""
    svdUser = models.CharField(_("Name_Birthday of the svdUser"), max_length=63, unique=True)
    email = models.EmailField(_("Email valid for the User of the this website"),
                              max_length=255, blank=True, null=True)
    name = models.CharField(_("First or Lastname"), max_length=47, default="")
    birthday = models.DateField(_("Birthday of the user"), null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = SvdUserManager()
    USERNAME_FIELD = 'svdUser'

    # @property
    # def name():
    #     pass


class Member(StampedBaseModel):
    class Sex(models.TextChoices):
        UNASSIGNED = (
            "U",
            _("Unassigned"),
        )
        MAN = (
            "M",
            _("Man"),
        )
        FEMALE = (
            "F",
            _("Female"),
        )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.CharField(
        _("First name"),
        max_length=63,
        help_text=_(
            "The first name(s) as stated in your passport or ID-card or given at birth"
        ),
    )
    lastname = models.CharField(_("Last Name"), max_length=63)
    call_name = models.CharField(_("Call name"), max_length=15, blank=True)
    sex = models.CharField(
        max_length=3,
        choices=Sex,
        default=Sex.UNASSIGNED,
        verbose_name=_("Gender by birth"),
        db_comment=_("Can be UNASSIGNED, MAN or FEMALE."),
        help_text=_("A modern choice is Unassigned"),
    )
    birthday = models.DateField(
        _("Date of Birth"),
        null=True,
        blank=True,
        help_text=_("Please use the following format: <em><strong>YYYY-MM-DD</strong><em>.")
    )
    birthday_txt = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )

    """
        As everybody has a father and a mother you see these can not be zero, but they are not
        always know.
        So they can point both to zero of to one of them. Normally they are not zero
        The person can also have different parents as there biological parents.
        This will be covered in 'Family'
        A person can have only one biological father and mother, therefor foreignkey is used
    """

    father = models.ForeignKey(
        to="self",
        on_delete=models.PROTECT,
        related_query_name="bio_father",
        verbose_name=_("Biological father"),
        limit_choices_to={"sex": "M"},
        help_text=_("If not known leave it blank!"),
        null=True,
        blank=True,
    )
    mother = models.ForeignKey(
        to="self",
        on_delete=models.PROTECT,
        related_name="bio_mother",
        verbose_name=_("Biological mother"),
        limit_choices_to={"sex": "F"},
        help_text=_("If not known leave it blank!"),
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-birthday_txt", "lastname"]

    @property
    def only_birthday_year(self):
        if self.birthday:
            return f"{self.birthday:%Y}"
        else:
            return _("Unknown")

    def __str__(self):
        return f"{self.lastname.upper():15s}{self.call_name:24s}  ({self.only_birthday_year})"
