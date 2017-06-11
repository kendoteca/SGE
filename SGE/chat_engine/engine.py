import json

from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.module_loading import import_string
from channels.sessions import channel_session
from channels import Group

from . import messages
from . import conf
from GE.models import InitialAttention, Alerta, AttentionType, Registers, SellPlace, Sucursal, Configuration, Persona


@channel_session
def on_connect(message):
    payload = message.content['text']
    message.channel_session['user'] = payload['username']
    Group('chat').add(message.reply_channel)


@channel_session
def on_disconnect(message):
    Group('chat').discard(message.reply_channel)
    Group('chat').send(messages.system(
        _('User %(user)s left chat') % message.channel_session))


def check_alert():

    turnos = len(InitialAttention.objects.filter(
        created__contains=timezone.localdate()
    ))

    registros = len(Registers.objects.filter(
        start_attention__gt=timezone.localdate()
    ))
    difference = turnos - registros
    configurations = Configuration.objects.all()[0]

    alerta = Alerta.objects.filter(
        starting_alert__contains=timezone.localdate(),
        finish_alert=None,
    ).exists()
    from django.core.mail import send_mail
    if difference >= configurations.generar_alarma_con_cantidad and not alerta:
        Alerta.objects.create(
            starting_alert=timezone.now(),
            finish_alert=None,
            sellplace=SellPlace.objects.get(id_sellplace=1),
            sucursal=Sucursal.objects.get(id_sucursal=1)
        )

        send_mail(
            'ALERTA ATENCION SUCURSAL Santa Ana N12',
            configurations.email,
            'pepe@intento.com',
            [configurations.email_destino],
            fail_silently=False
        )
    elif difference < configurations.generar_alarma_con_cantidad and alerta:
        update_alert = Alerta.objects.get(
            starting_alert__contains=timezone.localdate(),
            finish_alert=None,
        )

        send_mail(
            'ALERTA ATENCION SUCURSAL Santa Ana N12',
            'La Alerta a Finalizado. Se inicializo a las {} y finalizo a las {}'.format(
                update_alert.starting_alert,
                timezone.now()
            ),
            'pepe@intento.com',
            [configurations.email_destino],
            fail_silently=False
        )

        update_alert.finish_alert = timezone.now()

        update_alert.save()


@channel_session
def on_message(message):
    payload = message.content['text']
    user = message.channel_session['user']
    sender = message.content['text']['user']
    import ipdb; ipdb.set_trace()
    persona = ''

    try:
        pin = message.content['text']['pin']
    except KeyError:
        pin = None

    if pin:
        persona = Persona.objects.get(pin=message.content['text']['pin'])

    if user == 'totem':

        attention = AttentionType.objects.get(name=message.content['text']['text'])

        try:
            last_attention = InitialAttention.objects.filter(
                attention_type=attention
            ).order_by('-id_initial_attention')[0]
        except Exception as e:
            last_attention = None

        if last_attention and (timezone.now().date() == last_attention.created.date()):
            initial_atention = InitialAttention.objects.create(
                attention_number=last_attention.attention_number+1,
                attention_type=attention,
            )
        else:
            initial_atention = InitialAttention.objects.create(
                attention_number=1,
                attention_type=attention,
            )

        message.content['text']['text'] = '{},{}'.format(
            initial_atention.attention_type.name,
            initial_atention.attention_number
        )
    elif user == 'atencion':
        att = AttentionType.objects.get(name=message.content['text']['text'])
        if message.content['text'].get('atencion_prioritaria_booleano') and sender == 'atencion':
            attention = InitialAttention.objects.get(
                attention_type=att,
                attention_number=message.content['text']['numero_atencion'],
                created__contains=timezone.localdate()
            )
            Registers.objects.create(
                pin=persona,
                attention_number=attention,
                priority_attention=message.content['text'].get('atencion_prioritaria_booleano'),
                attention_type=att,
                start_attention=timezone.now(),
                observations='',
                finish_attention=timezone.now(),
                sellplace=SellPlace.objects.get(id_sellplace=1),
                sucursal=Sucursal.objects.get(id_sucursal=1),
            )
        elif message.content['text'].get('atencion_prioritaria_booleano') and sender == 'update':
            attention = InitialAttention.objects.get(
                attention_type=att,
                attention_number=message.content['text']['numero_atencion'],
                created__contains=timezone.localdate()
            )
            register = Registers.objects.get(attention_type=att, attention_number=attention)
            register.finish_attention = timezone.now()
            register.observations = message.content['text']['observaciones']
            register.save()

        if sender == 'update' and not message.content['text'].get('atencion_prioritaria_booleano'):
            attention = InitialAttention.objects.get(
                attention_type=att,
                attention_number=message.content['text']['numero'],
                created__contains=timezone.localdate()
            )
            register = Registers.objects.get(attention_type=att, attention_number=attention)
            register.finish_attention = timezone.now()
            register.observations = message.content['text']['observaciones']
            register.save()
        elif not message.content['text'].get('atencion_prioritaria_booleano'):
            hola = Registers.objects.filter(
                attention_type=att,
                priority_attention=False,
                start_attention__gt=timezone.localdate()
            )
            if len(hola) == 0:
                lolo = InitialAttention.objects.filter(
                    attention_type=att,
                    created__gt=timezone.localdate()
                ).order_by('id_initial_attention')[0]
                message.content['text']['text'] = '{},{},{}'.format(
                    att.name,
                    lolo.attention_number,
                    message.content['text']['puesto']
                )
                message = messages.info(payload['text'], sender if sender == 'visualizador' else user)
                Group('chat').send(message)
                if sender != 'visualizador':
                    Registers.objects.create(
                        pin=persona,
                        attention_number=lolo,
                        priority_attention=False,
                        attention_type=att,
                        start_attention=timezone.now(),
                        observations='',
                        finish_attention=timezone.now(),
                        sellplace=SellPlace.objects.get(id_sellplace=1),
                        sucursal=Sucursal.objects.get(id_sucursal=1),
                    )
            else:
                if sender == 'cantidad':
                    text = message.content['text']['text']

                    message.content['text']['text'] = '{},{}'.format(
                            sender,
                            text
                    )
                else:
                    last = hola.order_by('-id_register')[0]
                    number_to_be_attend = '',
                    next_number = 0
                    check_number = len(InitialAttention.objects.filter(
                        attention_number__gt=last.attention_number.attention_number,
                        attention_type=att,
                        created__gt=timezone.localdate()
                    ))

                    for number in range(1, check_number+1):
                        number_to_be_attend = InitialAttention.objects.get(
                            attention_number=last.attention_number.attention_number+number,
                            attention_type=att,
                            created__gt=timezone.localdate()
                        )
                        if not Registers.objects.filter(
                            attention_number=number_to_be_attend,
                            attention_type=att,
                            start_attention__gt=timezone.localdate()
                        ).exists():
                            next_number = last.attention_number.attention_number+number
                            break
                    if next_number != 0:
                        puesto = message.content['text']['puesto']
                        message.content['text']['text'] = '{},{},{}'.format(
                            att.name,
                            next_number,
                            puesto
                        )
                        message = messages.info(payload['text'], sender if sender == 'visualizador' else user)
                        Group('chat').send(message)
                        if sender != 'visualizador':
                            Registers.objects.create(
                                pin=persona,
                                attention_number=number_to_be_attend,
                                priority_attention=False,
                                attention_type=att,
                                start_attention=timezone.now(),
                                observations='',
                                finish_attention=timezone.now(),
                                sellplace=SellPlace.objects.get(id_sellplace=1),
                                sucursal=Sucursal.objects.get(id_sucursal=1),
                            )

    check_alert()
    message = messages.info(payload['text'], user)
    Group('chat').send(message)


@channel_session
def on_command(message):
    payload = message.content['text']
    user = message.channel_session['user']
    command, *args = payload['text'].strip().split()

    if command == '/me' and len(args) >= 1:
        text = ' '.join(args)
        message = messages.info('{} {}'.format(user, text))
        Group('chat').send(message)

    else:
        msg = messages.system(
            _(
                'Error: no such command %(command)s '
                'with arguments "%(args)s"'
            ) % {'command': command, 'args': ' '.join(args)})
        message.reply_channel.send(msg)


def get_engine():
    return import_string(conf.CHAT_ENGINE)
