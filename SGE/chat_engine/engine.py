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


@channel_session
def on_message(message):
    payload = message.content['text']
    user = message.channel_session['user']
    if message.content['text']['user'] == 'visualizador':
        puesto = message.content['text']['puesto']
        attention_number = message.content['text']['attention_number']
        attention_type = message.content['text']['text']

        # att = AttentionType.objects.get(name=message.content['text']['text'])
        # hola = Registers.objects.filter(
        #     attention_type=att,
        #     priority_attention=False,
        #     start_attention__gt=timezone.now().date()
        # )
        # number_to_be_attend = ''
        # next_number = 0
        # # import ipdb; ipdb.set_trace()

        # if len(hola) == 0:
        #     lolo = InitialAttention.objects.filter(
        #         attention_type=att,
        #         created__gt=timezone.now().date()
        #     ).order_by('id_initial_attention')[0]

        #     next_number = lolo.attention_number
        # else:

        #     last = hola.order_by('-id_register')[0]
        #     check_number = len(InitialAttention.objects.filter(
        #         attention_number__gt=last.attention_number.attention_number,
        #         attention_type=att,
        #         created__gt=timezone.now().date()
        #     ))

        #     for number in range(1, check_number+1):
        #         number_to_be_attend = InitialAttention.objects.get(
        #             attention_number=last.attention_number.attention_number+number,
        #             attention_type=att,
        #             created__gt=timezone.now().date()
        #         )
        #         if not Registers.objects.filter(
        #             attention_number=number_to_be_attend,
        #             attention_type=att,
        #             start_attention__gt=timezone.now().date()
        #         ).exists():
        #             next_number = last.attention_number.attention_number+number
        #             break

        message.content['text']['text'] = '{},{},{}'.format(
            attention_type,
            attention_number,
            puesto
        )

    message = messages.info(payload['text'], user)
    Group('chat').send(message)


    # sender = message.content['text']['user']
    # persona = ''

    # try:
    #     pin = message.content['text']['pin']
    # except KeyError:
    #     pin = None

    # if pin:
    #     persona = Persona.objects.get(pin=message.content['text']['pin'])

    # if user == 'atencion':
    #     att = AttentionType.objects.get(name=message.content['text']['text'])
    #     if message.content['text'].get('atencion_prioritaria_booleano') and sender == 'atencion':
    #         attention = InitialAttention.objects.get(
    #             attention_type=att,
    #             attention_number=message.content['text']['numero_atencion'],
    #             created__contains=timezone.localdate()
    #         )
    #         Registers.objects.create(
    #             pin=persona,
    #             attention_number=attention,
    #             priority_attention=message.content['text'].get('atencion_prioritaria_booleano'),
    #             attention_type=att,
    #             start_attention=timezone.now(),
    #             observations='',
    #             finish_attention=timezone.now(),
    #             sellplace=SellPlace.objects.get(id_sellplace=1),
    #             sucursal=Sucursal.objects.get(id_sucursal=1),
    #         )
    #     elif message.content['text'].get('atencion_prioritaria_booleano') and sender == 'update':
    #         attention = InitialAttention.objects.get(
    #             attention_type=att,
    #             attention_number=message.content['text']['numero_atencion'],
    #             created__contains=timezone.localdate()
    #         )
    #         register = Registers.objects.get(attention_type=att, attention_number=attention)
    #         register.finish_attention = timezone.now()
    #         register.observations = message.content['text']['observaciones']
    #         register.save()

    #     if sender == 'update' and not message.content['text'].get('atencion_prioritaria_booleano'):
    #         attention = InitialAttention.objects.get(
    #             attention_type=att,
    #             attention_number=message.content['text']['numero'],
    #             created__contains=timezone.localdate()
    #         )
    #         register = Registers.objects.get(attention_type=att, attention_number=attention)
    #         register.finish_attention = timezone.now()
    #         register.observations = message.content['text']['observaciones']
    #         register.save()
    #     elif not message.content['text'].get('atencion_prioritaria_booleano'):
    #         hola = Registers.objects.filter(
    #             attention_type=att,
    #             priority_attention=False,
    #             start_attention__gt=timezone.localdate()
    #         )
    #         if len(hola) == 0:
    #             lolo = InitialAttention.objects.filter(
    #                 attention_type=att,
    #                 created__gt=timezone.localdate()
    #             ).order_by('id_initial_attention')[0]
    #             message.content['text']['text'] = '{},{},{}'.format(
    #                 att.name,
    #                 lolo.attention_number,
    #                 message.content['text']['puesto']
    #             )
    #             message = messages.info(payload['text'], sender if sender == 'visualizador' else user)
    #             Group('chat').send(message)
    #             if sender != 'visualizador':
    #                 Registers.objects.create(
    #                     pin=persona,
    #                     attention_number=lolo,
    #                     priority_attention=False,
    #                     attention_type=att,
    #                     start_attention=timezone.now(),
    #                     observations='',
    #                     finish_attention=timezone.now(),
    #                     sellplace=SellPlace.objects.get(id_sellplace=1),
    #                     sucursal=Sucursal.objects.get(id_sucursal=1),
    #                 )
    #         else:
    #             if sender == 'cantidad':
    #                 text = message.content['text']['text']

    #                 message.content['text']['text'] = '{},{}'.format(
    #                         sender,
    #                         text
    #                 )
    #             else:
    #                 last = hola.order_by('-id_register')[0]
    #                 number_to_be_attend = '',
    #                 next_number = 0
    #                 check_number = len(InitialAttention.objects.filter(
    #                     attention_number__gt=last.attention_number.attention_number,
    #                     attention_type=att,
    #                     created__gt=timezone.localdate()
    #                 ))

    #                 for number in range(1, check_number+1):
    #                     number_to_be_attend = InitialAttention.objects.get(
    #                         attention_number=last.attention_number.attention_number+number,
    #                         attention_type=att,
    #                         created__gt=timezone.localdate()
    #                     )
    #                     if not Registers.objects.filter(
    #                         attention_number=number_to_be_attend,
    #                         attention_type=att,
    #                         start_attention__gt=timezone.localdate()
    #                     ).exists():
    #                         next_number = last.attention_number.attention_number+number
    #                         break
    #                 if next_number != 0:
    #                     puesto = message.content['text']['puesto']
    #                     message.content['text']['text'] = '{},{},{}'.format(
    #                         att.name,
    #                         next_number,
    #                         puesto
    #                     )
    #                     message = messages.info(payload['text'], sender if sender == 'visualizador' else user)
    #                     Group('chat').send(message)
    #                     if sender != 'visualizador':
    #                         Registers.objects.create(
    #                             pin=persona,
    #                             attention_number=number_to_be_attend,
    #                             priority_attention=False,
    #                             attention_type=att,
    #                             start_attention=timezone.now(),
    #                             observations='',
    #                             finish_attention=timezone.now(),
    #                             sellplace=SellPlace.objects.get(id_sellplace=1),
    #                             sucursal=Sucursal.objects.get(id_sucursal=1),
    #                         )

    # check_alert()


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
