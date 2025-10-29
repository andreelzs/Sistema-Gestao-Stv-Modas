from django.contrib import admin
from .models import Beneficiario

@admin.register(Beneficiario)
class BeneficiarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'data_nascimento', 'idade', 'genero', 'cidade', 'ativo', 'data_cadastro')
    search_fields = ('nome_completo', 'cpf', 'cidade', 'bairro')
    list_filter = ('ativo', 'genero', 'escolaridade', 'cidade', 'data_cadastro')
    readonly_fields = ('data_cadastro', 'idade') 

    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'data_nascimento', 'genero', 'cpf', 'rg', 'ativo')
        }),
        ('Endereço', {
            'fields': ('cep', 'logradouro', 'numero_endereco', 'complemento_endereco', 'bairro', 'cidade', 'estado'),
            'classes': ('collapse',) 
        }),
        ('Contato', {
            'fields': ('telefone_principal', 'telefone_secundario', 'email'),
            'classes': ('collapse',)
        }),
        ('Informações Socioeconômicas e Educacionais', {
            'fields': ('escolaridade', 'ocupacao', 'renda_familiar_aproximada'),
            'classes': ('collapse',)
        }),
        ('Outras Informações', {
            'fields': ('como_conheceu_ong', 'observacoes', 'data_cadastro'),
            'classes': ('collapse',)
        }),
    )
