from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Adicionado para paginação
from django.db.models import F # Adicionado para ordenação com nulls_last
from .models import Tarefa
from .forms import FormularioTarefa
from voluntarios.models import Voluntario # Para filtros ou informações adicionais
from contas.decorators import admin_required # Importar o decorator

@login_required
def listar_tarefas(request):
    # Adicionar filtros
    # Parâmetros de filtro e ordenação
    filtro_status_param = request.GET.get('status')
    filtro_voluntario_id = request.GET.get('voluntario')
    termo_pesquisa_titulo = request.GET.get('q_titulo')
    ordenacao_prazo_param = request.GET.get('ordenar_por_prazo')
    aba_selecionada = request.GET.get('aba', 'ativas') # Padrão para 'ativas'

    tarefas_qs = Tarefa.objects.all()

    # Filtragem baseada na aba selecionada
    if aba_selecionada == 'concluidas':
        tarefas_qs = tarefas_qs.filter(status='CONC')
        titulo_pagina = 'Tarefas Concluídas'
        # Ordenação específica para tarefas concluídas
        tarefas_ordenadas = tarefas_qs.order_by('-data_conclusao_efetiva', '-prioridade', 'titulo')
    else: # aba_selecionada == 'ativas'
        tarefas_qs = tarefas_qs.exclude(status='CONC')
        titulo_pagina = 'Tarefas Ativas'
        # Aplicar filtros de status (exceto 'CONC'), voluntário e título para tarefas ativas
        if termo_pesquisa_titulo:
            tarefas_qs = tarefas_qs.filter(titulo__icontains=termo_pesquisa_titulo)
        if filtro_status_param: # Não aplicar filtro de status 'CONC' aqui
            tarefas_qs = tarefas_qs.filter(status=filtro_status_param)
        if filtro_voluntario_id:
            tarefas_qs = tarefas_qs.filter(voluntario_responsavel_id=filtro_voluntario_id)

        # Lógica de Ordenação para tarefas ativas
        if ordenacao_prazo_param == 'asc':
            tarefas_ordenadas = tarefas_qs.order_by(F('data_prevista_conclusao').asc(nulls_last=True), '-prioridade', 'titulo')
        elif ordenacao_prazo_param == 'desc':
            tarefas_ordenadas = tarefas_qs.order_by(F('data_prevista_conclusao').desc(nulls_last=True), '-prioridade', 'titulo')
        else:
            # Ordenação padrão para tarefas ativas
            tarefas_ordenadas = tarefas_qs.order_by('-prioridade', F('data_prevista_conclusao').asc(nulls_last=True), 'titulo')
            
    paginator = Paginator(tarefas_ordenadas, 10) # 10 tarefas por página
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    voluntarios_ativos = Voluntario.objects.filter(ativo=True)
    
    status_choices_filtrado = Tarefa.STATUS_TAREFA
    if aba_selecionada == 'ativas':
        status_choices_filtrado = [s for s in Tarefa.STATUS_TAREFA if s[0] != 'CONC']

    contexto = {
        'page_obj': page_obj,
        'titulo_pagina': titulo_pagina,
        'status_choices': status_choices_filtrado,
        'voluntarios_ativos': voluntarios_ativos,
        'filtro_status_atual': filtro_status_param if aba_selecionada == 'ativas' else None,
        'filtro_voluntario_atual': int(filtro_voluntario_id) if filtro_voluntario_id else None,
        'termo_pesquisa_titulo_atual': termo_pesquisa_titulo,
        'ordenacao_prazo_atual': ordenacao_prazo_param if aba_selecionada == 'ativas' else None,
        'aba_atual': aba_selecionada,
        'is_paginated': True
    }
    return render(request, 'tarefas/listar_tarefas.html', contexto)

@login_required
def cadastrar_tarefa(request):
    if request.method == 'POST':
        form = FormularioTarefa(request.POST, user=request.user) # Passar user
        if form.is_valid():
            try:
                tarefa = form.save(commit=False)
                tarefa.atribuido_por = request.user # Usuário logado que criou a tarefa
                if tarefa.status == 'CONC' and not tarefa.data_conclusao_efetiva:
                    tarefa.data_conclusao_efetiva = timezone.now().date()
                tarefa.save()
                form.save_m2m() # Adicionado para salvar relações ManyToMany
                messages.success(request, 'Tarefa cadastrada com sucesso!')
                return redirect('tarefas:listar_tarefas')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao cadastrar a tarefa: {e}')
    else:
        form = FormularioTarefa(user=request.user) # Passar user
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Cadastrar Nova Tarefa'
    }
    return render(request, 'tarefas/formulario_tarefa.html', contexto)

@login_required
def detalhar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    contexto = {
        'tarefa': tarefa,
        'titulo_pagina': f'Detalhes da Tarefa: {tarefa.titulo}'
    }
    return render(request, 'tarefas/detalhar_tarefa.html', contexto)

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    if request.method == 'POST':
        form = FormularioTarefa(request.POST, instance=tarefa, user=request.user) # Passar user
        if form.is_valid():
            try:
                tarefa_editada = form.save(commit=False)
                # Se o status for mudado para Concluída e não houver data de conclusão, preenche
                if tarefa_editada.status == 'CONC' and not tarefa_editada.data_conclusao_efetiva:
                    tarefa_editada.data_conclusao_efetiva = timezone.now().date()
                # Se o status for mudado de Concluída para outro, limpa a data de conclusão
                elif tarefa.status == 'CONC' and tarefa_editada.status != 'CONC':
                     tarefa_editada.data_conclusao_efetiva = None
                tarefa_editada.save()
                form.save_m2m() # Adicionado para salvar relações ManyToMany
                messages.success(request, 'Tarefa atualizada com sucesso!')
                return redirect('tarefas:detalhar_tarefa', tarefa_id=tarefa.id)
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao atualizar a tarefa: {e}')
    else:
        form = FormularioTarefa(instance=tarefa, user=request.user) # Passar user
    
    contexto = {
        'form': form,
        'tarefa': tarefa,
        'titulo_pagina': f'Editar Tarefa: {tarefa.titulo}'
    }
    return render(request, 'tarefas/formulario_tarefa.html', contexto)

@login_required
@admin_required # Apenas admin pode excluir tarefas
def excluir_tarefa(request, tarefa_id): # Ou cancelar/arquivar
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    if request.method == 'POST':
        try:
            tarefa.delete()
            messages.success(request, f'Tarefa "{tarefa.titulo}" excluída com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao excluir/cancelar a tarefa: {e}')
        return redirect('tarefas:listar_tarefas')
    
    contexto = {
        'tarefa': tarefa,
        'titulo_pagina': f'Confirmar Exclusão da Tarefa: {tarefa.titulo}'
    }
    return render(request, 'tarefas/confirmar_exclusao_tarefa.html', contexto)

# View para atualizar status rapidamente 
@login_required
def atualizar_status_tarefa(request, tarefa_id, novo_status):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    if novo_status in [s[0] for s in Tarefa.STATUS_TAREFA]:
        tarefa.status = novo_status
        if novo_status == 'CONC' and not tarefa.data_conclusao_efetiva:
            tarefa.data_conclusao_efetiva = timezone.now().date()
        elif tarefa.status == 'CONC' and novo_status != 'CONC': 
            tarefa.data_conclusao_efetiva = None
        tarefa.save()
        messages.success(request, f'Status da tarefa "{tarefa.titulo}" atualizado para "{tarefa.get_status_display()}".')
    else:
        messages.error(request, 'Status inválido.')
    return redirect(request.META.get('HTTP_REFERER', 'tarefas:listar_tarefas'))
