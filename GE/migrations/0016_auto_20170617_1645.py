# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-17 16:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0015_attentiontype_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registers',
            name='duracion',
            field=models.IntegerField(default=0),
        ),
    ]
