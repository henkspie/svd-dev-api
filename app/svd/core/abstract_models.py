from django.conf import settings
from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class StampedBaseModel(TimeStampedModel):
    note = models.CharField(max_length=255, blank=True)
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.PROTECT
    )

    class Meta:
        abstract = True
