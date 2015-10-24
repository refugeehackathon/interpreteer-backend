# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0007_userprofile_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 24, 21, 46, 38, 742902, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
