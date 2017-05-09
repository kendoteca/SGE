# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 07:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GE', '0002_auto_20170507_0750'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AtentionType',
            new_name='AttentionType',
        ),
        migrations.RenameModel(
            old_name='Configurations',
            new_name='Configuration',
        ),
        migrations.RenameModel(
            old_name='Promosions',
            new_name='Promotion',
        ),
        migrations.RenameField(
            model_name='attentiontype',
            old_name='id_atention',
            new_name='id_attention',
        ),
        migrations.RenameField(
            model_name='configuration',
            old_name='aleatory_promosion',
            new_name='aleatory_promotion',
        ),
        migrations.RenameField(
            model_name='configuration',
            old_name='print_promosions',
            new_name='print_promotions',
        ),
        migrations.RenameField(
            model_name='promotion',
            old_name='id_promosion',
            new_name='id_promotion',
        ),
        migrations.RenameField(
            model_name='promotion',
            old_name='promosion_message',
            new_name='promotion_message',
        ),
        migrations.RenameField(
            model_name='registers',
            old_name='finish_atention',
            new_name='finish_attention',
        ),
        migrations.RenameField(
            model_name='registers',
            old_name='start_atention',
            new_name='start_attention',
        ),
        migrations.RemoveField(
            model_name='registers',
            name='atention_number',
        ),
        migrations.AddField(
            model_name='registers',
            name='attention_number',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GE.AttentionType'),
            preserve_default=False,
        ),
    ]
