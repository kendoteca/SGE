from GE.models import Persona, InitialAttention, Registers, AttentionType

from GE.models import InitialAttention, Registers, AttentionType, SellPlace, Sucursal

from django.db.models import Sum, Avg, Count, Max
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from GE.api_service.serializers import RegistersSerializer, PersonaSerializers, InitialAttentionSerializers


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def rgisters_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        # snippets = Registers.objects.filter(**kwargs)
        # serializer = RegistersSerializer(snippets, many=True)
        # return JSONResponse(serializer.data)
        return
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RegistersSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)


@csrf_exempt
def registers_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Registers.objects.get(pk=pk)
    except Registers.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RegistersSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RegistersSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)


@csrf_exempt
def user_pin(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """

    try:
        snippet = Persona.objects.get(pin=pk)
    except Persona.DoesNotExist:
        return HttpResponse('false', content_type='application/json')

    if request.method == 'GET':
        return JSONResponse(snippet.check_pin(int(pk)))


@csrf_exempt
def crear_turno(request):
    """
    Crea turno cuando seleccionan una opcion en totem
    """

    if request.method == 'POST':
        attention = AttentionType.objects.get(name=request.POST['tipo_atencion'])
        try:
            last_attention = InitialAttention.objects.filter(
                attention_type=attention,
                created__contains=timezone.now().date()
            ).order_by('-id_initial_attention')[0]
        except Exception as e:
            last_attention = None

        if last_attention and (timezone.now().date() == last_attention.created.date()):
            initial_atention = InitialAttention.objects.create(
                attention_number=last_attention.attention_number+1,
                attention_type=attention,
                created=timezone.now()
            )
        else:
            initial_atention = InitialAttention.objects.create(
                attention_number=1,
                attention_type=attention,
                created=timezone.now()
            )
        serializer = InitialAttentionSerializers(initial_atention)

        return JSONResponse(serializer.data, status=201)


@csrf_exempt
def consulta_estado(request):
    """
    consulta estados de turnos...
    """

    if request.method == 'GET':
        estado = dict()
        tipo_atenciones = AttentionType.objects.values('name')
        try:
            registros = Registers.objects.filter(start_attention__contains=timezone.now().date()).values('attention_type__name').annotate(Count('attention_number'))
        except Exception:
            registros = None

        try:
            atenciones = InitialAttention.objects.filter(created__contains=timezone.now().date()).values('attention_type__name').annotate(Count('attention_number'))
        except Exception:
            atenciones = None

        for atencion in atenciones:
            for registro in registros:
                if registro['attention_type__name'] == atencion['attention_type__name']:
                    tipo_estado = registro['attention_type__name']
                    estado[tipo_estado] = atencion['attention_number__count'] - registro['attention_number__count']

        for tipo_atencion in tipo_atenciones:
            if not tipo_atencion['name'] in estado:
                    estado[tipo_atencion['name']] = atenciones.get(attention_type__name=tipo_atencion['name'])['attention_number__count'] \
                        if atenciones.filter(attention_type__name=tipo_atencion['name']).exists() else \
                        0

    return JSONResponse(estado, status=201)


@csrf_exempt
def crear_registro(request):
    """
    Crea registro de turnos...
    """
    if request.method == 'POST':
        att = AttentionType.objects.get(name=request.POST['tipo_atencion'])
        if request.POST['pin']:
            persona = Persona.objects.get(pin=request.POST['pin'])
        try:
            numero = visualizador(request).content

            atencion = InitialAttention.objects.get(attention_number=numero, attention_type=att, created__contains=timezone.now().date())

            registro_guardado = Registers.objects.create(
                pin=persona,
                attention_number=atencion,
                priority_attention=False,
                attention_type=att,
                start_attention=timezone.now(),
                observations=request.POST['tipo_atencion'] if 'tipo_atencion' in request.POST else '',
                finish_attention=timezone.now(),
                sellplace=SellPlace.objects.get(id_sellplace=1),
                sucursal=Sucursal.objects.get(id_sucursal=1),
            )
            serializer = RegistersSerializer(registro_guardado)
        except ValueError:
            return JSONResponse('No hay turnos para ser Atendidos!', status=400)

    return JSONResponse(serializer.data, status=201)


@csrf_exempt
def actualiza_registro(request, id):
    """
    actualiza un registro y le pone la hora de finalizacion...
    """
    if request.method == 'GET':
        try:
            registro = Registers.objects.get(id_register=id)
            registro.finish_attention = timezone.now()
            registro.save()
        except Exception:
            registro = None
        serializer = RegistersSerializer(registro)
    return JSONResponse(serializer.data, status=201)


@csrf_exempt
def atencion_prioritaria(request):
    """
   crea un registro de atencion prioritaria
    """
    if request.method == 'POST':
        persona = Persona.objects.get(pin=request.POST['pin'])
        att = AttentionType.objects.get(name=request.POST['tipo_atencion'])
        atencion = InitialAttention.objects.get(attention_number=request.POST['numero_atencion'], attention_type=att, created__contains=timezone.now().date())
        if not Registers.objects.filter(attention_number=atencion, start_attention__contains=timezone.now().date(), attention_type=att).exists():
            try:
                registro = Registers.objects.create(
                    pin=persona,
                    attention_number=atencion,
                    priority_attention=True,
                    attention_type=att,
                    start_attention=timezone.now(),
                    observations=request.POST['tipo_atencion'] if 'tipo_atencion' in request.POST else '',
                    finish_attention=timezone.now(),
                    sellplace=SellPlace.objects.get(id_sellplace=1),
                    sucursal=Sucursal.objects.get(id_sucursal=1),
                )
                serializer = RegistersSerializer(registro)
            except Exception:
                return JSONResponse('El turno ya fue Atendido!', status=400)
            serializer = RegistersSerializer(registro)
        else:
            return JSONResponse('El turno ya fue Atendido!', status=400)
    return JSONResponse(serializer.data, status=201)


@csrf_exempt
def visualizador(request):
    """
    Número a llamar o a crear Registro
    """
    # import ipdb; ipdb.set_trace()
    # att = AttentionType.objects.get(name=request.POST['tipo_atencion'])

    # ultimo = Registers.objects.filter(
    #     attention_type=att,
    #     start_attention__contains=timezone.now().date(),
    #     priority_attention=False
    # ).values(
    #     'attention_type__name',
    #     'attention_number__attention_number'
    # ).annotate(Max('attention_number')).order_by('-attention_number')

    # if len(ultimo) > 0:

    #     atencion = InitialAttention.objects.filter(
    #         attention_type=att,
    #         attention_number__gt=ultimo['attention_number__attention_number']
    #     )

    #     cantidades = len(atencion)
    #     llamar = 0

    #     for cantidad in range(0, cantidades):
    #         if not Registers.objects.filter(
    #             attention_type=att,
    #             attention_number=atencion[cantidad],
    #             start_attention__contains=timezone.now().date()
    #         ).exists():
    #             llamar = atencion[cantidad].attention_number
    #             break
    att = AttentionType.objects.get(name=request.POST['tipo_atencion'])
    hola = Registers.objects.filter(
        attention_type=att,
        priority_attention=False,
        start_attention__gt=timezone.now().date()
    )
    number_to_be_attend = '',
    next_number = 0

    if len(hola) == 0:
        lolo = InitialAttention.objects.filter(
            attention_type=att,
            created__gt=timezone.now().date()
        ).order_by('id_initial_attention')[0]

        next_number = lolo.attention_number
    else:

        last = hola.order_by('-id_register')[0]
        check_number = len(InitialAttention.objects.filter(
            attention_number__gt=last.attention_number.attention_number,
            attention_type=att,
            created__gt=timezone.now().date()
        ))

        for number in range(1, check_number+1):
            number_to_be_attend = InitialAttention.objects.get(
                attention_number=last.attention_number.attention_number+number,
                attention_type=att,
                created__gt=timezone.now().date()
            )
            if not Registers.objects.filter(
                attention_number=number_to_be_attend,
                attention_type=att,
                start_attention__gt=timezone.now().date()
            ).exists():
                next_number = last.attention_number.attention_number+number
                break
        # if next_number != 0:


    return JSONResponse(next_number, status=201)


# def promedios(request):
#     tipo_atenciones = AttentionType.objects.values('name')
#     try:
#         promedio_por_tipo = Registers.objects.values('attention_type__name').annotate(Avg('duracion'))
#         for key, value in promedio_por_tipo:
#             dictionary[key] = value

#     except:
#         promedio_por_tipo = None

#     for tipo_atencion in tipo_atenciones:
#         for promedio in promedio_por_tipo:
#             if tipo_atencion['name'] promedio




