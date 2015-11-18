# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_board', '0004_auto_20151109_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='end_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='end_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='request',
            name='start_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
