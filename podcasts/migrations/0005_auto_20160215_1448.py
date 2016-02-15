# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0004_auto_20160214_2305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='unsubscribed',
            field=models.DateTimeField(help_text='The date on which the user unsubscribed from this podcast.', null=True),
        ),
    ]
