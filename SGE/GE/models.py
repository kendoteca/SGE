# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Persona(models.Model):
    id_persona = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin = models.IntegerField()

    def check_pin(self, pin_ingresado):
        return self.pin == pin_ingresado

    def __str__(self):
        return '{}, {}'.format(self.user.last_name, self.user.first_name)


class Configuration(models.Model):
    imprimir_promocion = models.BooleanField()
    promocion_aleatoria = models.BooleanField()
    generar_alarma_con_cantidad = models.IntegerField()
    email_destino = models.CharField(max_length=50)
    email = models.CharField(max_length=50)


class ConfiguracionesEstandar(models.Model):
    nombre_agencia = models.CharField(max_length=50)
    Color = models.CharField(max_length=50)
    images = models.CharField(max_length=200)
    sounds = models.CharField(max_length=200)


class Promotion(models.Model):
    id_promotion = models.AutoField(primary_key=True)
    promotion_message = models.CharField(max_length=50)

    def __str__(self):
        return str(self.promotion_message)


class SellPlace(models.Model):
    id_sellplace = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    people_attended = models.IntegerField()

    def __str__(self):
        return str(self.name)


class Sucursal(models.Model):
    id_sucursal = models.AutoField(primary_key=True)
    sucursal_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)

    def __str__(self):
        return str(self.sucursal_name)


class AttentionType(models.Model):
    id_attention_type = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Alerta(models.Model):
    id_alerta = models.AutoField(primary_key=True)
    starting_alert = models.DateTimeField(
        default=timezone.now
    )

    finish_alert = models.DateTimeField(
        blank=True,
        null=True
    )

    sellplace = models.ForeignKey(SellPlace)
    sucursal = models.ForeignKey(Sucursal)


class InitialAttention(models.Model):
    id_initial_attention = models.AutoField(primary_key=True)
    attention_number = models.IntegerField()
    attention_type = models.ForeignKey(AttentionType)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.attention_number)


class Registers(models.Model):
    id_register = models.AutoField(primary_key=True)
    pin = models.ForeignKey(Persona)
    priority_attention = models.BooleanField()
    attention_number = models.ForeignKey(InitialAttention)
    attention_type = models.ForeignKey(AttentionType)
    start_attention = models.DateTimeField(
        default=timezone.now
    )
    observations = models.TextField()

    finish_attention = models.DateTimeField()

    finish_total_attention = models.DateTimeField(blank=True, null=True)

    duracion = models.IntegerField(null=True)

    sellplace = models.ForeignKey(SellPlace)

    sucursal = models.ForeignKey(Sucursal)
