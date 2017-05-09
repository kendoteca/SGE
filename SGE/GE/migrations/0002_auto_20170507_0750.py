# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 07:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alerta',
            name='sellplace',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GE.SellPlace'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='alerta',
            name='sucursal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GE.Sucursal'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registers',
            name='sellplace',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GE.SellPlace'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registers',
            name='sucursal',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GE.Sucursal'),
            preserve_default=False,
        ),
    ]
