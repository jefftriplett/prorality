# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-19 04:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0010_auto_20171219_0358'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalproposal',
            name='hashid',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='hashid',
        ),
    ]
