"""
Svd database event and health models
"""
from django.db import models
from core.abstract_models import StampedBaseModel
from django.utils.translation import gettext_lazy as _

from core.models import Member


class EventList(models.Model):
    """
    List of events
    """
    event_type = models.CharField(_("Event type"), max_length=15)

    def __str__(self):
        return self.event_type


def get_event_types():
    event_list = [("birth", _("Birth")), ("DEATH", _("Death")),]
    query = EventList.objects.all()
    print(query)
    if query:
        for i in range(len(query)):
            event = str(query[i])
            trans_event = _(event)
            event_list.append((event.upper(), trans_event))
            print(event_list)
    return event_list


class Event(StampedBaseModel):
    """ Event happening in somebodies life. """
    event_type = models.CharField(max_length=15, choices=get_event_types)
    date = models.DateField(_("Date of the event"))
    place = models.CharField(_("Place where the Event happened"))
    source = models.ManyToManyField("Source")
    member = models.ForeignKey(
        to=Member,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.event_type


class Source(models.Model):
    """ Storage of documents etc """
    source_type = models.CharField(max_length=15)

    def __str__(self):
        return self.source_type
