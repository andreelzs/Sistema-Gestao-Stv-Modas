from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import Lower
from datetime import date, timedelta, datetime # Adicionado datetime para strptime
from voluntarios.models import Voluntario
from beneficiarios.models import Beneficiario
from tarefas.models import Tarefa
from cursos.models import Certificado # Adicionado para gráficos de cursos
import json # Para passar dados para o JavaScript

@login_required
def painel_principal(request):
    aba_param = request.GET.get('aba', 'voluntarios') # Padrão para 'voluntarios'

    # Dados para os gráficos
    # 1. Contagem de tarefas por status
    tarefas_por_status = Tarefa.objects.values('status').annotate(total=Count('status')).order_by('status')
    status_labels = [dict(Tarefa.STATUS_TAREFA).get(item['status'], item['status']) for item in tarefas_por_status]
    status_data = [item['total'] for item in tarefas_por_status]

    # 2. Contagem de voluntários 
    voluntarios_ativos = Voluntario.objects.filter(ativo=True).count()
    voluntarios_inativos = Voluntario.objects.filter(ativo=False).count()
    voluntario_status_labels = ['Ativos', 'Inativos']
    voluntario_status_data = [voluntarios_ativos, voluntarios_inativos]

    # --- DADOS DE BENEFICIÁRIOS (TODOS) ---
    beneficiarios_todos_qs = Beneficiario.objects.all()

    # 3. Todos os Beneficiários por Gênero
    beneficiarios_por_genero_todos = beneficiarios_todos_qs.values('genero').annotate(total=Count('genero')).order_by('genero')
    genero_labels_todos = [dict(Beneficiario.GENERO_CHOICES).get(item['genero'], item['genero']) for item in beneficiarios_por_genero_todos]
    genero_data_todos = [item['total'] for item in beneficiarios_por_genero_todos]
    
    # 4. Todos os Beneficiários por Escolaridade
    beneficiarios_por_escolaridade_todos = beneficiarios_todos_qs.values('escolaridade').annotate(total=Count('escolaridade')).order_by('escolaridade')
    escolaridade_labels_todos = [dict(Beneficiario.ESCOLARIDADE_CHOICES).get(item['escolaridade'], item['escolaridade']) for item in beneficiarios_por_escolaridade_todos]
    escolaridade_data_todos = [item['total'] for item in beneficiarios_por_escolaridade_todos]

    # --- DADOS DE BENEFICIÁRIOS (ATIVOS) ---
    beneficiarios_ativos_qs = Beneficiario.objects.filter(ativo=True)

    # 3.1. Beneficiários Ativos por Gênero
    beneficiarios_por_genero_ativos = beneficiarios_ativos_qs.values('genero').annotate(total=Count('genero')).order_by('genero')
    genero_labels_ativos = [dict(Beneficiario.GENERO_CHOICES).get(item['genero'], item['genero']) for item in beneficiarios_por_genero_ativos]
    genero_data_ativos = [item['total'] for item in beneficiarios_por_genero_ativos]

    # 4.1. Beneficiários Ativos por Escolaridade
    beneficiarios_por_escolaridade_ativos = beneficiarios_ativos_qs.values('escolaridade').annotate(total=Count('escolaridade')).order_by('escolaridade')
    escolaridade_labels_ativos = [dict(Beneficiario.ESCOLARIDADE_CHOICES).get(item['escolaridade'], item['escolaridade']) for item in beneficiarios_por_escolaridade_ativos]
    escolaridade_data_ativos = [item['total'] for item in beneficiarios_por_escolaridade_ativos]

    # 5. Contagem de voluntários por disponibilidade (dia/turno)
    dias_semana_map = {
        "Segunda": "seg", "Terça": "ter", "Quarta": "qua", 
        "Quinta": "qui", "Sexta": "sex", "Sábado": "sab", "Domingo": "dom"
    }
    turnos_map = {"Manhã": "m", "Tarde": "t", "Noite": "n"}
    
    disp_labels = list(dias_semana_map.keys())
    disp_datasets = []

    for nome_turno, abrev_turno in turnos_map.items():
        turno_data = []
        for nome_dia, abrev_dia in dias_semana_map.items():
            campo_filtro = f"disp_{abrev_dia}_{abrev_turno}" # Ajustar se o nome do campo for diferente
            count = Voluntario.objects.filter(ativo=True, **{campo_filtro: True}).count()
            turno_data.append(count)
        disp_datasets.append({
            "label": nome_turno,
            "data": turno_data,
        })

     # 6. Tarefas por Prioridade (Ativas)
    tarefas_ativas_por_prioridade = Tarefa.objects.exclude(status='CONC').values('prioridade').annotate(total=Count('id')).order_by('prioridade')
    prioridade_labels = [dict(Tarefa.PRIORIDADE_TAREFA).get(item['prioridade'], str(item['prioridade'])) for item in tarefas_ativas_por_prioridade]
    prioridade_data = [item['total'] for item in tarefas_ativas_por_prioridade]

    # 7. Beneficiários por Faixa Etária (TODOS)
    hoje = date.today()
    faixas_etarias_todos = {
        "0-10 anos": 0, "11-17 anos": 0, "18-25 anos": 0, 
        "26-35 anos": 0, "36-50 anos": 0, "51+ anos": 0, "Idade N/D": 0
    }
    for b in beneficiarios_todos_qs: # Usar queryset de todos
        if b.data_nascimento:
            idade = hoje.year - b.data_nascimento.year - ((hoje.month, hoje.day) < (b.data_nascimento.month, b.data_nascimento.day))
            if 0 <= idade <= 10: faixas_etarias_todos["0-10 anos"] += 1
            elif 11 <= idade <= 17: faixas_etarias_todos["11-17 anos"] += 1
            elif 18 <= idade <= 25: faixas_etarias_todos["18-25 anos"] += 1
            elif 26 <= idade <= 35: faixas_etarias_todos["26-35 anos"] += 1
            elif 36 <= idade <= 50: faixas_etarias_todos["36-50 anos"] += 1
            elif idade >= 51: faixas_etarias_todos["51+ anos"] += 1
        else:
            faixas_etarias_todos["Idade N/D"] += 1
    faixa_etaria_labels_todos = list(faixas_etarias_todos.keys())
    faixa_etaria_data_todos = list(faixas_etarias_todos.values())

    # 7.1. Beneficiários por Faixa Etária (ATIVOS)
    faixas_etarias_ativos = {
        "0-10 anos": 0, "11-17 anos": 0, "18-25 anos": 0, 
        "26-35 anos": 0, "36-50 anos": 0, "51+ anos": 0, "Idade N/D": 0
    }
    for b in beneficiarios_ativos_qs: # Usar queryset de ativos
        if b.data_nascimento:
            idade = hoje.year - b.data_nascimento.year - ((hoje.month, hoje.day) < (b.data_nascimento.month, b.data_nascimento.day))
            if 0 <= idade <= 10: faixas_etarias_ativos["0-10 anos"] += 1
            elif 11 <= idade <= 17: faixas_etarias_ativos["11-17 anos"] += 1
            elif 18 <= idade <= 25: faixas_etarias_ativos["18-25 anos"] += 1
            elif 26 <= idade <= 35: faixas_etarias_ativos["26-35 anos"] += 1
            elif 36 <= idade <= 50: faixas_etarias_ativos["36-50 anos"] += 1
            elif idade >= 51: faixas_etarias_ativos["51+ anos"] += 1
        else:
            faixas_etarias_ativos["Idade N/D"] += 1
    faixa_etaria_labels_ativos = list(faixas_etarias_ativos.keys())
    faixa_etaria_data_ativos = list(faixas_etarias_ativos.values())

    # 8. Beneficiários por Localização (Cidade) - Top 10 (TODOS)
    benef_por_cidade_todos = beneficiarios_todos_qs.annotate(cidade_lower=Lower('cidade')).values('cidade_lower').annotate(total=Count('id')).order_by('-total').filter(cidade_lower__isnull=False)[:10]
    cidade_labels_todos = [item['cidade_lower'].title() if item['cidade_lower'] else "N/D" for item in benef_por_cidade_todos]
    cidade_data_todos = [item['total'] for item in benef_por_cidade_todos]

    # 8.1. Beneficiários por Localização (Cidade) - Top 10 (ATIVOS)
    benef_por_cidade_ativos = beneficiarios_ativos_qs.annotate(cidade_lower=Lower('cidade')).values('cidade_lower').annotate(total=Count('id')).order_by('-total').filter(cidade_lower__isnull=False)[:10]
    cidade_labels_ativos = [item['cidade_lower'].title() if item['cidade_lower'] else "N/D" for item in benef_por_cidade_ativos]
    cidade_data_ativos = [item['total'] for item in benef_por_cidade_ativos]


    # 9. Beneficiários por Renda Familiar Aproximada (TODOS)
    faixas_renda_todos = {
        "Até R$1.500": 0, "R$1.501 - R$3.000": 0,
        "R$3.001 - R$5.000": 0, "Acima de R$5.000": 0, "Não Informado": 0
    }
    for b in beneficiarios_todos_qs: # Usar queryset de todos
        if b.renda_familiar_aproximada is not None:
            if b.renda_familiar_aproximada <= 1500: faixas_renda_todos["Até R$1.500"] += 1
            elif 1501 <= b.renda_familiar_aproximada <= 3000: faixas_renda_todos["R$1.501 - R$3.000"] += 1
            elif 3001 <= b.renda_familiar_aproximada <= 5000: faixas_renda_todos["R$3.001 - R$5.000"] += 1
            else: faixas_renda_todos["Acima de R$5.000"] += 1
        else:
            faixas_renda_todos["Não Informado"] += 1
    renda_labels_todos = list(faixas_renda_todos.keys())
    renda_data_todos = list(faixas_renda_todos.values())

    # 9.1. Beneficiários por Renda Familiar Aproximada (ATIVOS)
    faixas_renda_ativos = {
        "Até R$1.500": 0, "R$1.501 - R$3.000": 0,
        "R$3.001 - R$5.000": 0, "Acima de R$5.000": 0, "Não Informado": 0
    }
    for b in beneficiarios_ativos_qs: # Usar queryset de ativos
        if b.renda_familiar_aproximada is not None:
            if b.renda_familiar_aproximada <= 1500: faixas_renda_ativos["Até R$1.500"] += 1
            elif 1501 <= b.renda_familiar_aproximada <= 3000: faixas_renda_ativos["R$1.501 - R$3.000"] += 1
            elif 3001 <= b.renda_familiar_aproximada <= 5000: faixas_renda_ativos["R$3.001 - R$5.000"] += 1
            else: faixas_renda_ativos["Acima de R$5.000"] += 1
        else:
            faixas_renda_ativos["Não Informado"] += 1
    renda_labels_ativos = list(faixas_renda_ativos.keys())
    renda_data_ativos = list(faixas_renda_ativos.values())

    # 10. Certificados por Curso (com filtro de período opcional)
    cert_data_inicio_param = request.GET.get('cert_data_inicio')
    cert_data_fim_param = request.GET.get('cert_data_fim')

    cert_por_curso_qs = Certificado.objects.all()

    if cert_data_inicio_param:
        try:
            data_inicio_obj = datetime.strptime(cert_data_inicio_param, '%Y-%m-%d').date()
            cert_por_curso_qs = cert_por_curso_qs.filter(data_emissao_certificado__gte=data_inicio_obj)
        except ValueError:
            pass # Ignorar data inválida
    
    if cert_data_fim_param:
        try:
            data_fim_obj = datetime.strptime(cert_data_fim_param, '%Y-%m-%d').date()
            cert_por_curso_qs = cert_por_curso_qs.filter(data_emissao_certificado__lte=data_fim_obj)
        except ValueError:
            pass # Ignorar data inválida

    cert_por_curso = cert_por_curso_qs.values('curso__nome_curso').annotate(total=Count('id')).order_by('-total')
    curso_cert_labels = [item['curso__nome_curso'] for item in cert_por_curso]
    curso_cert_data = [item['total'] for item in cert_por_curso]
    
    hoje = date.today() # Já definido acima, mas pode ser redefinido para clareza ou movido
    data_inicio_ultimo_mes = hoje - timedelta(days=30)

    contexto = {
        'titulo_pagina': 'Dashboard Principal',
        'total_voluntarios': Voluntario.objects.filter(ativo=True).count(), # Alterado para ativos
        'total_beneficiarios': Beneficiario.objects.filter(ativo=True).count(), # Alterado para ativos
        'total_tarefas_pendentes': Tarefa.objects.filter(status='PEND').count(),
        'total_tarefas_concluidas': Tarefa.objects.filter(
            status='CONC', 
            data_conclusao_efetiva__gte=data_inicio_ultimo_mes,
            data_conclusao_efetiva__lte=hoje
        ).count(), # Alterado para o último mês
        
        # Passar os objetos Python diretamente, |json_script fará a serialização
        'status_labels_json': status_labels,
        'status_data_json': status_data,
        'voluntario_status_labels_json': voluntario_status_labels,
        'voluntario_status_data_json': voluntario_status_data,
        
        'genero_labels_todos_json': genero_labels_todos,
        'genero_data_todos_json': genero_data_todos,
        'escolaridade_labels_todos_json': escolaridade_labels_todos,
        'escolaridade_data_todos_json': escolaridade_data_todos,
        'faixa_etaria_labels_todos_json': faixa_etaria_labels_todos,
        'faixa_etaria_data_todos_json': faixa_etaria_data_todos,
        'cidade_labels_todos_json': cidade_labels_todos,
        'cidade_data_todos_json': cidade_data_todos,
        'renda_labels_todos_json': renda_labels_todos,
        'renda_data_todos_json': renda_data_todos,

        'genero_labels_ativos_json': genero_labels_ativos,
        'genero_data_ativos_json': genero_data_ativos,
        'escolaridade_labels_ativos_json': escolaridade_labels_ativos,
        'escolaridade_data_ativos_json': escolaridade_data_ativos,
        'faixa_etaria_labels_ativos_json': faixa_etaria_labels_ativos,
        'faixa_etaria_data_ativos_json': faixa_etaria_data_ativos,
        'cidade_labels_ativos_json': cidade_labels_ativos,
        'cidade_data_ativos_json': cidade_data_ativos,
        'renda_labels_ativos_json': renda_labels_ativos,
        'renda_data_ativos_json': renda_data_ativos,
        
        'disp_labels_json': disp_labels,
        'disp_datasets_json': disp_datasets,

        'prioridade_labels_json': prioridade_labels,
        'prioridade_data_json': prioridade_data,
        'curso_cert_labels_json': curso_cert_labels,
        'curso_cert_data_json': curso_cert_data,

        # Para preencher os filtros de data no template
        'cert_data_inicio_form': cert_data_inicio_param,
        'cert_data_fim_form': cert_data_fim_param,
        'aba_atual': aba_param, # Passar a aba atual para o template
    }
    return render(request, 'dashboard/painel_principal.html', contexto)
