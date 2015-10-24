from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from geoposition.fields import GeopositionField


class Location(models.Model):
    location = GeopositionField()
    zip_code = models.CharField(max_length=5)


class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email_address = models.EmailField(unique=True)
    mobility = models.PositiveIntegerField(blank=True, null=True)  # range of mobility in km
    location = models.ForeignKey(Location, related_name="users", null=True)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email_address', 'zip_code']


class Language(models.Model):
    language_code = models.CharField(max_length=255, unique=True, choices=settings.LANGUAGES)


class TranslationSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="translation_skills")
    source_language = models.ForeignKey(Language, related_name="source_languages")
    destination_language = models.ForeignKey(Language, related_name="destination_languages")


class LanguageSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="language_skills")
    language = models.ForeignKey(Language, related_name="language_skills")
    level = models.CharField(max_length=255, choices=settings.LANGUAGE_LEVELS)



