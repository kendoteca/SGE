# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-17 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0014_registers_duracion'),
    ]

    operations = [
        migrations.AddField(
            model_name='attentiontype',
            name='label',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
