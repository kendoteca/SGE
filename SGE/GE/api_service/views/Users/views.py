from GE.models import Registers, Persona

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from GE.api_service.serializers import RegistersSerializer, PersonaSerializers


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
        import ipdb; ipdb.set_trace()
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
