# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 03:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0010_persona'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='correo',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='department',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='nombre',
        ),
    ]