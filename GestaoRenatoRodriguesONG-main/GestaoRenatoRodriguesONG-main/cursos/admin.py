from django.contrib import admin
from .models import Curso, Certificado

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome_curso', 'descricao')
    search_fields = ('nome_curso', 'descricao')

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('beneficiario', 'curso', 'data_conclusao', 'data_emissao_certificado', 'certificado_recebido')
    search_fields = ('beneficiario__nome_completo', 'curso__nome_curso')
    list_filter = ('curso', 'data_conclusao', 'certificado_recebido')
    autocomplete_fields = ['beneficiario', 'curso'] # Facilita a seleção em admin com muitos registros
    date_hierarchy = 'data_conclusao'
