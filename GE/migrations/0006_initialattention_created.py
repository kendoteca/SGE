# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 06:02
from __future__ import unicode_literals

from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0005_initialattention_attention_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='initialattention',
            name='created',
            field=models.DateTimeField(default=timezone.now),
            preserve_default=False,
        ),
    ]