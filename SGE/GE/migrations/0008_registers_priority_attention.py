# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-03 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0007_auto_20170526_0635'),
    ]

    operations = [
        migrations.AddField(
            model_name='registers',
            name='priority_attention',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
