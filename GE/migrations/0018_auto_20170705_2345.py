# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-05 23:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0017_auto_20170705_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registers',
            name='duracion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='registers',
            name='duracion_atencion',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4),
        ),
    ]
