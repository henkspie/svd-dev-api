"""
Svd database event and health models
"""
from django.db import models
from core.abstract_models import StampedBaseModel, TimeStampedModel
from django.utils.translation import gettext_lazy as _

from core.models import Member, member_image_filepath


class EventList(models.Model):
    """
    List of events
    """
    event_type = models.CharField(_("Event type"), max_length=15)

    def __str__(self):
        return self.event_type


def get_event_types():
    event_list = [("BIRTH", _("Birth")), ("DEATH", _("Death")),]
    query = EventList.objects.all()
    # print(query)
    if query:
        for i in range(len(query)):
            event = str(query[i])
            trans_event = _(event)
            event_list.append((event.upper(), trans_event))
            # print(event_list)
    return event_list


class Events(StampedBaseModel):
    """ Event happening in somebodies life. """
    event_type = models.CharField(max_length=15, choices=get_event_types)
    date = models.DateField(_("Date of the event"))
    end_date = models.DateField(_("End date of the event"), null=True, blank=True)
    source = models.ManyToManyField("Source", blank=True)
    image = models.ImageField(null=True, blank=True, upload_to=member_image_filepath)
    member = models.ForeignKey(
        to=Member,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.event_type


class Location(TimeStampedModel):
    """ Storage of documents etc """
    name = models.CharField(_("Name of the location"), max_length=31, unique=True)
    city = models.CharField(_("Name of the town"), max_length=31, null=True, blank=True)
    street = models.CharField(_("Street"), max_length=127, null=True, blank=True)
    number = models.CharField(_("House or Apartment number"), max_length=15, null=True, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=15, null=True, blank=True)
    country = models.CharField(_("Country"), max_length=15, default=_("Netherlands"))
    long = models.DecimalField(_("GPS Longitude"),
                               max_digits=9, decimal_places=6, null=True, blank=True)
    lat = models.DecimalField(_("GPS Latitude"),
                              max_digits=9, decimal_places=6, null=True, blank=True)
    events = models.ForeignKey(
        to=Events,
        on_delete=models.DO_NOTHING,
        related_name=_("Location"),
        # help_text=_(f"Location where {member} was/is {event_type}"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    @property
    def address(self):
        return f"{self.street}, {self.number}, {self.city}, {self.postal_code}"


class Source(models.Model):
    """ Storage of documents etc """
    source_type = models.CharField(max_length=15)

    def __str__(self):
        return self.source_type
