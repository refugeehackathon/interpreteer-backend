# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_board', '0003_auto_20151025_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='requires_presence',
            field=models.BooleanField(default=False),
        ),
    ]
