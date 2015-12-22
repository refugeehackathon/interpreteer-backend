# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    def set_coords(apps, schema_editor):
        Location = apps.get_model("user_management", "Location")
        for location in Location.objects.all():
            location.latitude = location.location.latitude
            location.longitude = location.location.longitude
            location.save()


    dependencies = [
        ('user_management', '0008_auto_20151024_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='latitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='location',
            name='longitude',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.RunPython(set_coords),
        migrations.RemoveField(
            model_name='location',
            name='location',
        ),
    ]
