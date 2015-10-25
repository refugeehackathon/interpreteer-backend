# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import models

# Create your models here.
from user_management.models import Language, Location


DIRECTION_CHOICES = (
    (0, "required to known"),
    (1, "known to required"),
    (2, "both"),
)


TYPE_CHOICES = (
    (0, "visit authorities"),
    (1, "letter"),
)


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="requests")
    required_language = models.ForeignKey(Language, related_name="required_by")
    known_languages = models.ManyToManyField(Language, related_name="known_for_request")
    direction = models.PositiveSmallIntegerField(choices=DIRECTION_CHOICES)
    kind = models.IntegerField(choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.ForeignKey(Location, related_name="requests")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    requires_presence = models.BooleanField()


class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="offers")
    location = models.ForeignKey(Location, related_name="offers")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    kind = models.IntegerField(choices=TYPE_CHOICES)
