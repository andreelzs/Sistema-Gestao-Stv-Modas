from django.db import models
from django.conf import settings

class Etiqueta(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=20)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)

    def __str__(self):
        return self.nome_completo
