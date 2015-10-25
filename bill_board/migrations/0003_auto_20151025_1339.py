# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bill_board', '0002_auto_20151025_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='title',
            field=models.CharField(default='default offer', max_length=255),
            preserve_default=False,
        ),
    ]
