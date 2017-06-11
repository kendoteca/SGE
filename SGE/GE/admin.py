# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Configuration,
    Promotion,
    SellPlace,
    Sucursal,
    AttentionType,
    InitialAttention,
    Alerta,
    Persona,
    Registers,
)


class RegistersAdmin(admin.ModelAdmin):
    list_display = (
        'pin',
        'attention_number',
        'attention_type',
        'start_attention',
        'observations',
        'finish_attention',
        'finish_total_attention',
        'duracion',
        'priority_attention',
        'sellplace',
        'sucursal'
    )
    list_filter = (
        'pin',
        'attention_type',
        'start_attention',
        'observations',
        'finish_attention',
        'finish_total_attention',
        'priority_attention',
        'sellplace',
        'sucursal'
    )
    search_fields = (
        'pin',
        'attention_number',
        'attention_type',
        'start_attention',
        'observations',
        'finish_attention',
        'finish_total_attention',
        'priority_attention',
        'sellplace',
        'sucursal'
    )


class InitialAttentionAdmin(admin.ModelAdmin):
    list_display = ('id_initial_attention', 'attention_number', 'attention_type', 'created')
    # list_filter = ('id_initial_attention', 'attention_number', 'attention_type', 'created')
    search_fields = ('id_initial_attention', 'attention_number', 'attention_type', 'created')

    def attention(self, obj):
        return '{}'.format(obj.attention_type.name)

    attention.short_description = 'name'


class AttentionTypeAdmin(admin.ModelAdmin):
    list_display = ('id_attention_type', 'name')
    # list_filter = ('id_initial_attention', 'attention_number', 'attention_type', 'created')
    search_fields = ('id_attention_type', 'name')

# Register your models here.
admin.site.register(
    Configuration,
)
admin.site.register(
    Promotion,
)
admin.site.register(
    Persona,
)
admin.site.register(
    SellPlace,
)
admin.site.register(
    Sucursal,
)
admin.site.register(
    AttentionType,
    AttentionTypeAdmin
)
admin.site.register(
    Alerta,
)
admin.site.register(
    InitialAttention,
    InitialAttentionAdmin
)
admin.site.register(
    Registers,
    RegistersAdmin,
)
