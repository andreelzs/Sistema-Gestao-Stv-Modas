from django.contrib import admin
from .models import Cliente, Etiqueta

@admin.register(Etiqueta)
class EtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'telefone', 'cidade')
    search_fields = ('nome_completo', 'usuario__username', 'telefone', 'cidade', 'cep')
    filter_horizontal = ('etiquetas',)
