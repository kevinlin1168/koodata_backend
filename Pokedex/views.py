from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from http import HTTPStatus

from .models import Pokemon, Type
# Create your views here.
def variablesValidation(value):
    if value:
        return True
    else:
        return False

def createJsonResponse(status, errorReason = '', data = {}, safe=True):
    responseBody = {
        'isSuccess': status == HTTPStatus.OK,
        'error': errorReason,
        'data': data
    }
    response = JsonResponse(responseBody, safe=safe)
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

def getTypeName(typeObjList):
    try:
        types = []
        for typeObj in typeObjList:
            types.append(typeObj.type_name)
        return types
    except:
        raise Exception("Get Types Error")
def getEvolutionObj(evolutionObj):
    return getPokemon(evolutionObj)

def getEvolutions(evolutionObjList):
    try:
        evolutions = []
        for evolutionObj in evolutionObjList:
            evolutions.append(getEvolutionObj(evolutionObj))
        return evolutions
    except:
        raise Exception("Get Evolutions Error")

def getPokemon(pokemonObj):
    types = getTypeName(pokemonObj.types.all())
    evolutions = getEvolutions(pokemonObj.evolutions.all())
    pokemon = {
        'number': pokemonObj.number,
        'name': pokemonObj.name,
        'types': types,
        'evolutions': evolutions
    }
    return pokemon



def create(request):
    form = request.POST or None
    if form: #check request method
        number = form.get('number')
        name = form.get('name')
        types = form.getlist('type')


        if (not variablesValidation(number)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables number")
        elif (not variablesValidation(name)):
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables name")
        elif (not variablesValidation(types)):
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables type")
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
                return createJsonResponse(HTTPStatus.OK, '', data)

            except IntegrityError:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'Try to create pokemon of same number or name')

            except:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")


def update(request):
    form = request.POST or None
    if form: #check request method
        id = form.get('id')
        number = form.get('number')
        name = form.get('name')
        types = form.getlist('type')

        if (not variablesValidation(id)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "id")
        elif (not variablesValidation(number)): 
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables number")
        elif (not variablesValidation(name)):
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables name")
        elif (not variablesValidation(types)):
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables type")
        else: #update pokemon
            try:
                pokemon = Pokemon.objects.get(id=id)
                pokemon.number = number
                pokemon.name = name
                pokemon.save()
                for typeName in types:
                    
                    #check if type exist
                    type = Type.objects.filter(type_name=typeName)
                    
                    if not type:
                        addType(typeName)

                
                pokemon.types.clear()
                for typeName in types:
                    type = Type.objects.get(type_name=typeName)
                    pokemon.types.add(type)
                return createJsonResponse(HTTPStatus.OK, '', data)

            except ObjectDoesNotExist:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'The id do not exist')
            except IntegrityError:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'Try to update pokemon of same number or name')
            except:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")

def retrieve(request):
    form = request.POST or None
    if form: #check request method
        id = form.get('id')
        if (not variablesValidation(id)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables id")
        try:
            return createJsonResponse(HTTPStatus.OK, '', getPokemon(pokemonObj))

        
        except ObjectDoesNotExist:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'The id do not exist')
        except:
            return createJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")


def retrieveByType(request):
    form = request.POST or None
    if form: #check request method
        types = form.getlist('type')
        if (not variablesValidation(types)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables type")
        try:
            responseData = []
            pokemonObjList = Pokemon.objects.filter(types__type_name__in = types)
            for pokemonObj in pokemonObjList:
                responseData.append(getPokemon(pokemonObj))
            return createJsonResponse(HTTPStatus.OK, '', responseData, False)
                
        except:
            return createJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")


def addEvolution(request):
    form = request.POST or None
    if form: #check request method
        pokemonID = form.get('pokemonID')
        evolutionID = form.get('evolutionID')
        if (not variablesValidation(pokemonID)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables pokemonID")
        elif (not variablesValidation(evolutionID)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables evolutionID")
        try:
            pokemon = Pokemon.objects.get(id=pokemonID)
            evolutionPokemon = Pokemon.objects.get(id=evolutionID)
            pokemon.evolutions.add(evolutionPokemon)
            return createJsonResponse(HTTPStatus.OK)
        except ObjectDoesNotExist:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'The id of pokemon or evolution do not exist')
        except:
            return createJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")

def deleteEvolution(request):
    form = request.POST or None
    if form: #check request method
        pokemonID = form.get('pokemonID')
        evolutionID = form.get('evolutionID')
        if (not variablesValidation(pokemonID)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables pokemonID")
        elif (not variablesValidation(evolutionID)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables evolutionID")
        try:
            try:
                pokemon = Pokemon.objects.get(id=pokemonID)
                evolutionPokemon = Pokemon.objects.get(id=evolutionID)
            except ObjectDoesNotExist:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'The id of pokemon or evolution do not exist')
            if(Pokemon.objects.filter(id = pokemonID, evolutions__id__in = evolutionID)):
                pokemon.evolutions.remove(evolutionPokemon)
            else:
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'The evolution do not exist')
            return createJsonResponse(HTTPStatus.OK)

        except:
            return createJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")

def deletePokemon(request):
    form = request.POST or None
    if form: #check request method
        id = form.get('id')
        if (not variablesValidation(id)): #check variables
            return createJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables id")
        try:
            if (Pokemon.objects.filter(evolutions__id__in = id)):
                return createJsonResponse(HTTPStatus.BAD_REQUEST, 'Can not delete Pokemon which is evolution of other Pokemon')
            else:
                pokemon = Pokemon.objects.get(id = id)
                pokemon.delete()
                return createJsonResponse(HTTPStatus.OK)

        except ObjectDoesNotExist:
            return createJsonResponse(HTTPStatus.BAD_REQUEST, 'The id of pokemon do not exist')
        except:
            return createJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")