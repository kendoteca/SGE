# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Configuration(models.Model):
    color = models.CharField(max_length=50)
    images = models.CharField(max_length=200)
    sounds = models.CharField(max_length=200)
    print_promotions = models.BooleanField()
    aleatory_promotion = models.BooleanField()
    nombre_agencia = models.CharField(max_length=50)
    cant_espera = models.IntegerField()
    email_destino = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Promotion(models.Model):
    id_promotion = models.IntegerField()
    promotion_message = models.CharField(max_length=50)


class SellPlace(models.Model):
    id_sellplace = models.IntegerField()
    name = models.CharField(max_length=50)
    people_attended = models.IntegerField()


class Sucursal(models.Model):
    id_sucursal = models.IntegerField()
    sucursal_name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)


class AttentionType(models.Model):
    id_attention = models.IntegerField()
    name = models.CharField(max_length=50)


class Alerta(models.Model):
    id_alerta = models.IntegerField()
    starting_alert = models.DateTimeField(
        default=timezone.now
    )

    finish_alert = models.DateTimeField(
        blank=True,
        null=True
    )

    sellplace = models.ForeignKey(SellPlace)
    sucursal = models.ForeignKey(Sucursal)


class Registers(models.Model):
    id_register = models.IntegerField()
    attention_number = models.ForeignKey(AttentionType)
    start_attention = models.DateTimeField(
        default=timezone.now
    )
    observations = models.TextField()

    finish_attention = models.DateTimeField()

    sellplace = models.ForeignKey(SellPlace)

    sucursal = models.ForeignKey(Sucursal)
