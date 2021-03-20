from django.contrib import admin

# Register your models here.
from .models import Type, Pokemon

admin.site.register(Type)
admin.site.register(Pokemon)
