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
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    requires_presence = models.BooleanField(default=False)

    def __str__(self):
        return "<Request: %s, %s, %s, %s>" % (self.user.username, self.start_time, self.end_time, self.kind)

    def matching_offers(self):
        offers = Offer.objects.filter(kind=self.kind)
        if self.start_time is not None and self.end_time is not None:
            offers = offers.filter(
                start_time__lte=self.start_time,
                end_time__gte=self.end_time)
        if self.direction == 0:
            offers = offers.filter(
                user__translation_skills__source_language=self.required_language
            ).filter(
                user__translation_skills__destination_language_id__in=self.known_languages.values('id')
            )
        elif self.direction == 1:
            offers = offers.filter(
                user__translation_skills__source_language__in=self.known_languages.values('id')
            ).filter(
                user__translation_skills__destination_language_id=self.required_language
            )
        elif self.direction == 2:
            offers_1 = offers.filter(
                user__translation_skills__source_language=self.required_language
            ).filter(
                user__translation_skills__destination_language_id__in=self.known_languages.values('id')
            )
            offers_2 = offers.filter(
                user__translation_skills__source_language__in=self.known_languages.values('id')
            ).filter(
                user__translation_skills__destination_language_id=self.required_language
            )
            offers = offers_1 & offers_2
        return offers


class Offer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="offers")
    location = models.ForeignKey(Location, related_name="offers")
    kind = models.IntegerField(choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "<Offer: %s, %s, %s, %s>" % (self.user.username, self.start_time, self.end_time, self.kind)
