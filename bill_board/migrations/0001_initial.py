# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0002_auto_20151024_1229'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('kind', models.IntegerField(choices=[(0, b'visit authorities'), (1, b'letter')])),
                ('location', models.ForeignKey(related_name='offers', to='user_management.Location')),
                ('user', models.ForeignKey(related_name='offers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('direction', models.PositiveSmallIntegerField(choices=[(0, b'required to known'), (1, b'known to required'), (2, b'both')])),
                ('kind', models.IntegerField(choices=[(0, b'visit authorities'), (1, b'letter')])),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('start_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('requires_presence', models.BooleanField()),
                ('known_languages', models.ManyToManyField(related_name='known_for_request', to='user_management.Language')),
                ('location', models.ForeignKey(related_name='requests', to='user_management.Location')),
                ('required_language', models.ForeignKey(related_name='required_by', to='user_management.Language')),
                ('user', models.ForeignKey(related_name='requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
