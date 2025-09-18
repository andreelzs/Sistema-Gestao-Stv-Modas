from django.contrib import admin
from .models import Cliente, Etiqueta

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'telefone', 'cidade')
    search_fields = ('nome_completo', 'telefone')

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)