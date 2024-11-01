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

    return False

def check_and_normalize_svdUser(name):
    """ Check or create a svdUser"""
    svdUser=False
    if name:
        svdUser = check_normalize_svdUser(name)

    if svdUser is None:
        birthday = input(_("What is your birthday:"))
        print(f"What is your birthday")
        candidates = Member.objects.filter(birthday=birthday).values()
        if candidates:
            for name in candidates:
                print(candidates.lastname)
        else:
            print("No candidates")
    return svdUser


class SvdUserManager(BaseUserManager):
    """Manager fo SvdUsers."""

    def _create_user(self, svdUser, password, email, **extra_fields):
        """Create, save and return a new user."""
        svdUser = check_and_normalize_svdUser(svdUser)
        if not svdUser:
            raise NameError(_("Not a correct SvdUser name given."))
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


class Member(StampedBaseModel):
    class Gender(models.TextChoices):
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
    birth_gender = models.CharField(
        max_length=3,
        choices=Gender,
        default=Gender.UNASSIGNED,
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
    time_birth = models.TimeField(
        _("Time of Birth"),
        null=True,
        blank=True,
        help_text=_("Please use the following format: <em><strong>14:00:00</strong><em>.")
    )
    birthday_txt = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )
    death_date = models.DateField(
        blank=True,
        null=True,
        help_text=_(
            "Please use the following format: <em><strong>YYYY-MM-DD</strong></em>."
        ),
        verbose_name=_("Died"),
        # default="1111-11-11",
    )
    death_date_txt = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )

    """
        As everybody has a father and a mother you see these can not be zero, but they are not always know.
        So they can point both to zero of to one of them. Normally they are not zero
        The person can also have different parents as there biological parents. This will be covered in 'Family'
        A person can have only one biological father and mother, therefor foreignkey is used
    """

    father = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        related_query_name="bio_father",
        verbose_name=_("Biological father"),
        limit_choices_to={"birth_gender": "M"},
        help_text=_("If not known leave it blank!"),
        null=True,
        blank=True,
    )
    mother = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        related_name="bio_mother",
        verbose_name=_("Biological mother"),
        limit_choices_to={"birth_gender": "F"},
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

