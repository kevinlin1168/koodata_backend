from django.db import models

# Create your models here.
class Type(models.Model):
    type_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_name


class Pokemon(models.Model):
    number = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50, unique=True)
    types = models.ManyToManyField(Type)
    evolutions = models.ManyToManyField('Pokemon')

    def __str__(self):
        return self.name
