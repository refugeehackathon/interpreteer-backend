# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bill_board', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='request',
            name='duration',
        ),
        migrations.AddField(
            model_name='offer',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 11, 40, 41, 962116, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='request',
            name='end_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 25, 11, 40, 55, 528449, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
