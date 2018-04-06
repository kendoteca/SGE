# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-26 06:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0006_initialattention_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alerta',
            name='id',
        ),
        migrations.RemoveField(
            model_name='promotion',
            name='id',
        ),
        migrations.RemoveField(
            model_name='registers',
            name='id',
        ),
        migrations.RemoveField(
            model_name='sellplace',
            name='id',
        ),
        migrations.RemoveField(
            model_name='sucursal',
            name='id',
        ),
        migrations.AlterField(
            model_name='alerta',
            name='id_alerta',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='initialattention',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='promotion',
            name='id_promotion',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='registers',
            name='id_register',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sellplace',
            name='id_sellplace',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='id_sucursal',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]