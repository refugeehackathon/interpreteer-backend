# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_board', '0005_auto_20151118_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='location',
        ),
        migrations.RemoveField(
            model_name='request',
            name='location',
        ),
    ]
