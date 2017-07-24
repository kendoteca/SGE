# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.db.models import Sum, Avg

from .forms import SignUpForm, Configurations
from GE.models import (
    AttentionType,
    Configuration,
    InitialAttention,
    Promotion,
    Registers,
)
from django.utils import timezone

turno = {
        'farmacia': 0,
        'obra_social': 0,
        'pami': 0,
        'particular': 0,
}


def chat(request):
    return render(request, 'chat/chat.html')


def final(request):
    show_message = 'hidden'
    message = ''
    alert = ''
    if request.method == 'POST':
        try:
            numero, tipo = request.POST['final'].split('.')
            attention_object = AttentionType.objects.get(
                id_attention_type=tipo
            )

            number_object = InitialAttention.objects.get(
                attention_number=numero,
                attention_type=attention_object,
                created__contains=timezone.now().date()
            )

            register = Registers.objects.get(
                attention_number=number_object,
                attention_type=attention_object,
                finish_attention__contains=timezone.now().date()
            )

            register.finish_total_attention = timezone.now()

            register.duracion = (timezone.now() - number_object.created).seconds

            register.save()
            show_message = 'visible'
            alert = 'success'
            message = 'El turno Nº{} ha finalizado correctamente.'.format(numero)
        except Exception:
            alert = 'danger'
            message = 'Ha habido un error al processar el ticket. Reintente.'
            show_message = 'visible'
    return render(
        request,
        'final.html',
        {
            'show_message': show_message,
            'message': message,
            'alert': alert
        }
    )
    return render(request, 'final.html')


@login_required()
def home(request):
    try:
        puesto = request.user.username.split('-')[1]
    except Exception:
        return HttpResponseRedirect(reverse('login'))

    # att_obra = AttentionType.objects.get(name='obra_social')
    # att_particular = AttentionType.objects.get(name='particular')
    # att_perfumeria = AttentionType.objects.get(name='perfumeria')
    # att_pami = AttentionType.objects.get(name='pami')

    # # promedio_total = Registers.objects.aggregate(Avg('duracion'))
    # dictionary = dict()
    # try:
    #     promedio_por_tipo = Registers.objects.values('attention_type__name').annotate(Avg('duracion'))
    #     for key, value in promedio_por_tipo:
    #         dictionary[key] = value

    # except Exception:
    #     import ipdb; ipdb.set_trace()
    #     promedio_por_tipo = None

    # reg_obra = Registers.objects.filter(
    #     attention_type=att_obra,
    #     start_attention__contains=timezone.localdate()
    # ).count()
    # reg_particular = Registers.objects.filter(
    #     attention_type=att_particular,
    #     start_attention__contains=timezone.localdate()
    # ).count()
    # reg_perfumeria = Registers.objects.filter(
    #     attention_type=att_perfumeria,
    #     start_attention__contains=timezone.localdate()
    # ).count()
    # reg_pami = Registers.objects.filter(
    #     attention_type=att_pami,
    #     start_attention__contains=timezone.localdate()
    # ).count()

    # obra_social_quantity = InitialAttention.objects.filter(
    #     created__contains=timezone.localdate(),
    #     attention_type=att_obra
    # ).count()

    # pami_quantity = InitialAttention.objects.filter(
    #     created__contains=timezone.localdate(),
    #     attention_type=att_pami
    # ).count()
    # perfumeria_quantity = InitialAttention.objects.filter(
    #     created__contains=timezone.localdate(),
    #     attention_type=att_perfumeria
    # ).count()
    # particular_quantity = InitialAttention.objects.filter(
    #     created__contains=timezone.localdate(),
    #     attention_type=att_particular
    # ).count()
    tipo_atenciones = AttentionType.objects.all()
    promedios_atencion = Registers.objects.values('attention_type__name').annotate(Avg('duracion_atencion'))
    return render(request, 'atencion.html', {
        'puesto': puesto,
        'user': request.user,
        'tipo_atenciones': tipo_atenciones,
        'promedios_atencion': promedios_atencion,
    })


def main(request):
    return render(request, 'main.html', {})


def totem(request):
    tipo_atenciones = AttentionType.objects.all()
    promotion = Promotion.objects.get(promotion_selected=1)
    config = Configuration.objects.all()[0]
    return render(
        request,
        'totem.html',
        {
            'tipo_atenciones': tipo_atenciones,
            'promocion': promotion,
            'config': config
        }
    )


def visualizador(request):
    tipo_atenciones = AttentionType.objects.all()

    config = Configuration.objects.all()[0]

    return render(
        request,
        'visualizador2.html' if config.visualizador_standard else 'visualizador.html',
        {
            'tipo_atenciones': tipo_atenciones,
            'loop': range(1, 8)
        }
    )


@login_required()
def registros(request):
    return render(request, 'registros.html', {})


@login_required()
def menu(request):
    return render(request, 'menu.html', {})


def logout(request):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def login(request):
    message = 'hidden'
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
            if user.is_staff:
                from django.contrib.auth import authenticate, login
                autenticated_user = authenticate(username=user.username, password=request.POST['password'])
                login(request, autenticated_user)
                return HttpResponseRedirect(reverse('menu'))
            if user.check_password(request.POST['password']):
                from django.contrib.auth import authenticate, login
                autenticated_user = authenticate(username=user.username, password=request.POST['password'])
                login(request, autenticated_user)
                if 'visualizador' in user.username:
                    return HttpResponseRedirect(reverse('visualizador'))
                elif 'puesto' in user.username:
                    return HttpResponseRedirect(reverse('home'))

        except Exception:
            message = 'visible'
    return render(
        request,
        'login.html',
        {
            'message': message
        }
    )


def data(request):
    if len(request.POST.keys()) > 0:
        turno[str(request.POST['turno'])] = turno[str(request.POST['turno'])] + 1
        # luego de registrar el turno tengo que mandar el mensaje al chat
    return render(request, 'totem.html', {})


def signup(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = SignUpForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass

            # Process the data in form.cleaned_data
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            # At this point, user is a User object that has already been saved
            # to the database. You can continue to change its attributes
            # if you want to change other fields.
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            # Save new user attributes
            user.save()

            return HttpResponseRedirect(reverse('login'))  # Redirect after POST
    else:
        form = SignUpForm()

    data = {
        'form': form,
    }
    return render(request, 'signup.html', data)


@login_required()
def configurations(request):
    form = Configurations()

    data = {
        'form': form,
    }
    return render(request, 'configurations.html', data)


@login_required()
def personas(request):
    return render(request, 'reporte_personas.html')


@login_required()
def alertas(request):
    return render(request, 'alertas.html')

def prueba(request):
    return render(request, 'prueba.html')


def promociones(request):
    promociones = Promotion.objects.all()
    return render(
        request,
        'promociones.html',
        {
            'promociones': promociones,
        }
    )
