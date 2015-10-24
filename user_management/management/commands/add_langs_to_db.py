# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from user_management.models import Language

class Command(BaseCommand):
    """
    Adds all languages to database
    """
    def handle(self,*args,**kwargs):
        for lang in settings.LANGUAGES:
            Language.objects.get_or_create(language_code=lang[0])