# Dentro do arquivo: clientes/models.py

from django.conf import settings
from django.db import models

class Etiqueta(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    # No futuro, podemos adicionar um campo de cor para exibir as etiquetas
    # cor = models.CharField(max_length=7, default="#FFFFFF") 

    class Meta:
        verbose_name = "Etiqueta"
        verbose_name_plural = "Etiquetas"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    # A linha abaixo cria um vínculo direto com o sistema de login do Django.
    # Cada cliente terá um usuário correspondente para o login no portal.
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    
    # Campos de endereço
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    cep = models.CharField(max_length=10, blank=True, null=True)
    
    observacoes = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    # Nova linha para as etiquetas
    etiquetas = models.ManyToManyField(Etiqueta, blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome_completo