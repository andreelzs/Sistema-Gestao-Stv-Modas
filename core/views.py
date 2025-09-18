from django.shortcuts import render
from voluntarios.models import Voluntario
from beneficiarios.models import Beneficiario
from tarefas.models import Tarefa
from datetime import date, timedelta

def pagina_inicial(request):
    # Dados para os cards
    total_voluntarios_ativos = 0
    total_beneficiarios_ativos = 0
    total_tarefas_pendentes = 0
    total_tarefas_concluidas_ultimo_mes = 0
    mensagem_boas_vindas_display = '' 
    
    if request.user.is_authenticated:
        # Cálculos dos cards apenas se autenticado
        total_voluntarios_ativos = Voluntario.objects.filter(ativo=True).count()
        total_beneficiarios_ativos = Beneficiario.objects.filter(ativo=True).count()
        total_tarefas_pendentes = Tarefa.objects.filter(status='PEND').count()
        
        hoje = date.today()
        data_inicio_ultimo_mes = hoje - timedelta(days=30)
        total_tarefas_concluidas_ultimo_mes = Tarefa.objects.filter(
            status='CONC',
            data_conclusao_efetiva__gte=data_inicio_ultimo_mes,
            data_conclusao_efetiva__lte=hoje
        ).count()

        # Mensagem de boas-vindas
        nome_usuario = request.user.get_full_name()
        if not nome_usuario:
            nome_usuario = request.user.first_name
        
        # Tenta obter o nome do perfil Voluntario se os campos de User não estiverem preenchidos
        if not nome_usuario:
            try:
                voluntario_perfil = Voluntario.objects.get(usuario=request.user)
                if voluntario_perfil.nome_completo:
                    nome_usuario = voluntario_perfil.nome_completo
            except Voluntario.DoesNotExist:
                # Usuário não tem perfil de voluntário, ou nome_completo não preenchido
                pass # nome_usuario continua None ou com valor anterior

        if not nome_usuario:
            nome_usuario = request.user.username
            
        mensagem_boas_vindas_display = f'Bem vindo! Você está logado como: {nome_usuario}.'
    else:
        mensagem_boas_vindas_display = 'Faça login para acessar o sistema. Caso ainda não tenha uma conta, entre em contato com a administração da ONG.'


    contexto = {
        'titulo_pagina': 'Bem-vindo ao Sistema de Gestão da ONG Renato Rodrigues!',
        'mensagem_boas_vindas': mensagem_boas_vindas_display,
        'total_voluntarios_ativos': total_voluntarios_ativos,
        'total_beneficiarios_ativos': total_beneficiarios_ativos,
        'total_tarefas_pendentes': total_tarefas_pendentes,
        'total_tarefas_concluidas_ultimo_mes': total_tarefas_concluidas_ultimo_mes,
    }
    return render(request, 'core/pagina_inicial.html', contexto)
