from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from geoposition.fields import GeopositionField
from celery.worker.strategy import default
import requests

class Location(models.Model):
    location = GeopositionField()
    zip_code = models.CharField(max_length=5)

def query_zip_code(sender, instance, **kwargs):
    if not instance.zip_code.isdigit():
        return
    r = requests.get('http://api.zippopotam.us/de/%s' % instance.zip_code)
    if r.status_code == 200:
        result = r.json()['places'][0]
        instance.location.longitude = result['longitude']
        instance.location.latitude = result['latitude']
        instance.save()

post_save.connect(query_zip_code, sender=Location, dispatch_uid="query_zip_code")


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        user  = self.model(username=username,
                           email=self.normalize_email(email),
                           )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(unique=True)
    mobility = models.PositiveIntegerField(blank=True, null=True)  # range of mobility in km
    location = models.ForeignKey(Location, related_name="users", null=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Language(models.Model):
    """
    To fill the databse with languages run "python manage.py add_langs_to_db"
    """
    language_code = models.CharField(max_length=255, unique=True, choices=settings.LANGUAGES)

    def __str__(self):
        return self.language_code
    

class TranslationSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="translation_skills")
    source_language = models.ForeignKey(Language, related_name="source_languages")
    destination_language = models.ForeignKey(Language, related_name="destination_languages")


class LanguageSkill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="language_skills")
    language = models.ForeignKey(Language, related_name="language_skills")
    level = models.CharField(max_length=255, choices=settings.LANGUAGE_LEVELS)
