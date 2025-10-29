from django.db import models
from django.conf import settings


class Tarefa(models.Model):
    STATUS_TAREFA = [
        ('PEND', 'Pendente'),
        ('FAZE', 'Sendo feita'),
        ('CONC', 'Concluída'),
        ('CANC', 'Cancelada'), 
    ]

    PRIORIDADE_TAREFA = [
        (1, 'Baixa'),
        (2, 'Média'),
        (3, 'Alta'),
        (4, 'Urgente'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título da Tarefa')
    descricao = models.TextField(verbose_name='Descrição Detalhada')
    status = models.CharField(
        max_length=4,
        choices=STATUS_TAREFA,
        default='PEND',
        verbose_name='Status'
    )
    prioridade = models.IntegerField(
        choices=PRIORIDADE_TAREFA,
        default=2, 
        verbose_name='Prioridade'
    )
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    data_prevista_conclusao = models.DateField(blank=True, null=True, verbose_name='Prazo de Entrega')
    data_conclusao_efetiva = models.DateField(blank=True, null=True, verbose_name='Data de Conclusão Efetiva')
    
    voluntarios_responsaveis = models.ManyToManyField(
        'voluntarios.Voluntario',
        blank=True, # Uma tarefa pode ser criada sem voluntários inicialmente
        related_name='tarefas_responsaveis', # Novo related_name para evitar conflitos
        verbose_name='Voluntários Responsáveis'
    )
    
    atribuido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, # Usuário do sistema (Colaborador/Admin) que atribuiu
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Pode ser uma tarefa criada pelo próprio voluntário ou sistema
        related_name='tarefas_criadas',
        verbose_name='Atribuído Por'
    )
    
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações Adicionais')

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['-prioridade', 'data_prevista_conclusao', 'titulo'] # Ordenar por prioridade (maior primeiro), depois prazo

    def __str__(self):
        return f"{self.titulo} ({self.get_status_display()})"
