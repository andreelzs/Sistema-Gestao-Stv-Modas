from django.contrib import admin
from .models import Tarefa

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status', 'prioridade', 'display_voluntarios', 'data_prevista_conclusao', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'voluntarios_responsaveis__nome_completo') # Alterado para o campo M2M
    list_filter = ('status', 'prioridade', 'data_prevista_conclusao', 'data_criacao', 'voluntarios_responsaveis') # Alterado
    readonly_fields = ('data_criacao', 'data_conclusao_efetiva')
    date_hierarchy = 'data_criacao'
    filter_horizontal = ('voluntarios_responsaveis',) # Melhor widget para M2M no admin

    fieldsets = (
        (None, {
            'fields': ('titulo', 'descricao', 'status', 'prioridade')
        }),
        ('Responsáveis e Prazos', {
            'fields': ('voluntarios_responsaveis', 'atribuido_por', 'data_prevista_conclusao', 'data_conclusao_efetiva') # Alterado
        }),
        ('Outras Informações', {
            'fields': ('observacoes', 'data_criacao'),
            'classes': ('collapse',)
        }),
    )

    def display_voluntarios(self, obj):
        return ", ".join([voluntario.nome_completo for voluntario in obj.voluntarios_responsaveis.all()])
    display_voluntarios.short_description = 'Voluntários Responsáveis'
