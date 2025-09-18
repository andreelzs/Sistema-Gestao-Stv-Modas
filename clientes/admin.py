from django.contrib import admin
from .models import Voluntario

@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'rg', 'telefone', 'ativo', 'data_cadastro')
    search_fields = ('nome_completo', 'cpf', 'rg')
    list_filter = ('ativo', 'data_cadastro')
    readonly_fields = ('data_cadastro',)
    
    fieldsets = (
        (None, {
            'fields': ('usuario', 'nome_completo', 'cpf', 'rg', 'data_nascimento', 'ativo')
        }),
        ('Contato', {
            'fields': ('telefone', 
                       'cep', 'logradouro', 'numero_endereco', 'complemento_endereco', 
                       'bairro', 'cidade', 'estado')
        }),
        ('Detalhes da ONG', {
            'fields': ('areas_interesse',)
        }),
        ('Disponibilidade Semanal', {
            'fields': (
                ('disp_seg_m', 'disp_seg_t', 'disp_seg_n'),
                ('disp_ter_m', 'disp_ter_t', 'disp_ter_n'),
                ('disp_qua_m', 'disp_qua_t', 'disp_qua_n'),
                ('disp_qui_m', 'disp_qui_t', 'disp_qui_n'),
                ('disp_sex_m', 'disp_sex_t', 'disp_sex_n'),
                ('disp_sab_m', 'disp_sab_t', 'disp_sab_n'),
                ('disp_dom_m', 'disp_dom_t', 'disp_dom_n'),
            ),
            'classes': ('collapse',) 
        }),
        ('Datas Importantes', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',) 
        }),
    )

    raw_id_fields = ('usuario',)
