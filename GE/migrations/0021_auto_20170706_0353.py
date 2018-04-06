# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-06 03:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0020_alerta_observations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='user',
        ),
        migrations.AddField(
            model_name='persona',
            name='email',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='first_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='persona',
            name='last_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]