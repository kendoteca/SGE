# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-13 01:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0025_promociones_visualizador'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='tiempo_imagenes_visualizador',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='configuration',
            name='tiempo_promociones_visualizador',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
