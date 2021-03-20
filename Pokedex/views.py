from django.shortcuts import render

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

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
            print(evolutionObj)
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
        id = form.get('id')
        number = form.get('number')
        name = form.get('name')
        types = form.getlist('type')

        if (not variablesValidation(id)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "id")
        elif (not variablesValidation(number)): 
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

                pokemon = Pokemon.objects.get(id=id)
                print(name)
                pokemon.number = number
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
                response.status_code = HTTPStatus.OK
                return response

            except Exception as e:
                print(e)
                return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")

def retrieve(request):
    form = request.POST or None
    if form: #check request method
        id = form.get('id')
        if (not variablesValidation(id)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables id")
        try:
            pokemonObj = Pokemon.objects.get(id=id)
            response = JsonResponse(getPokemon(pokemonObj))
            response.status_code = HTTPStatus.OK
            return response
                
        except Exception as e:
            print(e)
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")


def retrieveByType(request):
    form = request.POST or None
    if form: #check request method
        types = form.getlist('type')
        if (not variablesValidation(types)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables type")
        try:
            responseData = []
            pokemonObjList = Pokemon.objects.filter(types__type_name__in = types)
            for pokemonObj in pokemonObjList:
                responseData.append(getPokemon(pokemonObj))
            response = JsonResponse(responseData, safe=False)
            response.status_code = HTTPStatus.OK
            return response
                
        except Exception as e:
            print(e)
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")


def addEvolution(request):
    form = request.POST or None
    if form: #check request method
        pokemonID = form.get('pokemonID')
        evolutionID = form.get('evolutionID')
        if (not variablesValidation(pokemonID)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables pokemonID")
        elif (not variablesValidation(evolutionID)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables evolutionID")
        try:
            pokemon = Pokemon.objects.get(id=pokemonID)
            evolutionPokemon = Pokemon.objects.get(id=evolutionID)
            if(pokemon and evolutionPokemon):
                pokemon.evolutions.add(evolutionPokemon)
            else:
                return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'Can not find pokemon')
            response = HttpResponse()
            response.status_code = HTTPStatus.OK
            return response
                
        except Exception as e:
            print(e)
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")

def deleteEvolution(request):
    form = request.POST or None
    if form: #check request method
        pokemonID = form.get('pokemonID')
        evolutionID = form.get('evolutionID')
        if (not variablesValidation(pokemonID)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables pokemonID")
        elif (not variablesValidation(evolutionID)): #check variables
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Missing variables evolutionID")
        try:
            pokemon = Pokemon.objects.get(id=pokemonID)
            evolutionPokemon = Pokemon.objects.get(id=evolutionID)
            if(pokemon and evolutionPokemon):
                pokemon.evolutions.remove(evolutionPokemon)
            else:
                return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'Can not find pokemon')
            response = HttpResponse()
            response.status_code = HTTPStatus.OK
            return response
                
        except Exception as e:
            print(e)
            return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, 'An exception occurred')

    else:
        return createErrorJsonResponse(HTTPStatus.BAD_REQUEST, "Request method error")