from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    Codigo = models.CharField(primary_key=True, max_length=10)
    Nombre = models.CharField(max_length=100)
    Creditos = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__ (self):
        texto = "{0} ({1})"
        return texto.format(self.Nombre, self.Creditos)