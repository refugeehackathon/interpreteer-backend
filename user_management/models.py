from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class UserProfile(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True)
    email_address = models.EmailField(unique=True)
    mobility = models.PositiveIntegerField(blank=True, null=True)  # range of mobility in km
    zip_code = models.CharField(max_length=5)

    location_long = models.FloatField(blank=True, null=True)
    location_lat = models.FloatField(blank=True, null=True)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email_address', 'zip_code']
