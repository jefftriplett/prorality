# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 05:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proposals', '0006_auto_20171121_0456'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproposal',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('final', 'Final'), ('withdrawn', 'Withdrawn'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='draft', max_length=16),
        ),
        migrations.AlterField(
            model_name='historicalvote',
            name='vote',
            field=models.IntegerField(blank=True, choices=[(1, '+1: Yes, I agree'), (2, "+0: I don't feel strongly about it, but I'm okay with this."), (3, "-0: I won't get in the way, but I'd rather we didn't do this."), (4, '-1: I object on the following grounds')], null=True),
        ),
        migrations.AlterField(
            model_name='proposal',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('final', 'Final'), ('withdrawn', 'Withdrawn'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='draft', max_length=16),
        ),
        migrations.AlterField(
            model_name='vote',
            name='vote',
            field=models.IntegerField(blank=True, choices=[(1, '+1: Yes, I agree'), (2, "+0: I don't feel strongly about it, but I'm okay with this."), (3, "-0: I won't get in the way, but I'd rather we didn't do this."), (4, '-1: I object on the following grounds')], null=True),
        ),
    ]
