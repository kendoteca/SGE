# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
	Configuration,
	Promotion,
	SellPlace,
	Sucursal,
	AttentionType,
	Alerta,
	Registers,
)

# Register your models here.
admin.site.register(
	Configuration,
)
admin.site.register(
	Promotion,
)
admin.site.register(
	SellPlace,
)
admin.site.register(
	Sucursal,
)
admin.site.register(
	AttentionType,
)
admin.site.register(
	Alerta,
)
admin.site.register(
	Registers,
)
