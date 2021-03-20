from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from http import HTTPStatus

from .models import Pokemon, Type
# Create your views here.
def variablesValidation(value):
    if value:
        return True
    else:
        return False

def createErrorJsonResponse(status, reason):
    response = JsonResponse({'error': reason})
    response.status_code = status
    return response

def addType(typeName):
    try:
        # add type
        type = Type(type_name=typeName)
        type.save()
        return True
    except:
        raise Exception("Add Types Error")


def create(request):
    form = request.POST or None
    if form: #check request method
        number = form.get('number')
        name = form.get('name')
        types = form.getlist('type')


        if (not variablesValidation(number)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables number")
        elif (not variablesValidation(name)):
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables name")
        elif (not variablesValidation(types)):
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables type")
        else: #create pokemon
            try:
                for typeName in types:
                    
                    #check if type exist
                    type = Type.objects.filter(type_name=typeName)
                    
                    if not type:
                        addType(typeName)

                pokemon = Pokemon(number = number, name = name)
                pokemon.save()
                for typeName in types:
                    type = Type.objects.get(type_name=typeName)
                    pokemon.types.add(type)
                data = {
                    'number': number,
                    'name': name,
                    'types': types
                }
                response = JsonResponse(data)
                response.status_code = HTTPStatus.CREATED
                return response

            except:
                return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")


def update(request):
    form = request.POST or None
    if form: #check request method
        number = form.get('number')
        name = form.get('name')
        types = form.getlist('type')


        if (not variablesValidation(number)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables number")
        elif (not variablesValidation(name)):
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables name")
        elif (not variablesValidation(types)):
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables type")
        else: #update pokemon
            try:
                for typeName in types:
                    
                    #check if type exist
                    type = Type.objects.filter(type_name=typeName)
                    
                    if not type:
                        addType(typeName)
                
                pokemon = Pokemon.objects.get(number=number)
                pokemon.name = name
                pokemon.save()
                pokemon.types.clear()
                for typeName in types:
                    type = Type.objects.get(type_name=typeName)
                    pokemon.types.add(type)
                data = {
                    'number': number,
                    'name': name,
                    'types': types
                }
                response = JsonResponse(data)
                response.status_code = HTTPStatus.CREATED
                return response

            except Exception as e:
                print(e)
                return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")