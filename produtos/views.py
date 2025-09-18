from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone # Adicionado para data_inativacao
from django.urls import reverse # Adicionado para construir URL com query string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Adicionado para paginação
from .models import Beneficiario
from .forms import FormularioBeneficiario
from contas.decorators import admin_required # Importar o decorator
from cursos.models import Certificado # Adicionar importação

@login_required
def listar_beneficiarios(request):
    termo_pesquisa_nome = request.GET.get('q_nome', None)
    filtro_ativo_param = request.GET.get('filtro_ativo', 'ativos') 
    
    if filtro_ativo_param == 'inativos':
        beneficiarios = Beneficiario.objects.filter(ativo=False)
        titulo_pagina_especifico = 'Beneficiários Inativos'
    else: # 'ativos' ou qualquer outro valor
        beneficiarios = Beneficiario.objects.filter(ativo=True)
        titulo_pagina_especifico = 'Beneficiários Ativos'
        filtro_ativo_param = 'ativos' # Garante que o valor seja 'ativos' se não for 'inativos'

    if termo_pesquisa_nome:
        beneficiarios = beneficiarios.filter(nome_completo__icontains=termo_pesquisa_nome)
    
    beneficiarios_list = beneficiarios.order_by('nome_completo') # Renomeado para evitar conflito com o page_obj

    paginator = Paginator(beneficiarios_list, 10) # 10 beneficiários por página
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        # Se a página não for um inteiro, entrega a primeira página.
        page_obj = paginator.page(1)
    except EmptyPage:
        # Se a página estiver fora do intervalo (ex: 9999), entrega a última página de resultados.
        page_obj = paginator.page(paginator.num_pages)
    
    contexto = {
        'page_obj': page_obj, # Objeto da página atual
        'titulo_pagina': titulo_pagina_especifico,
        'filtro_ativo_atual': filtro_ativo_param,
        'is_paginated': True # Para o template saber que há paginação
        # O template já acessa request.GET.q_nome para o valor do input de pesquisa
    }
    return render(request, 'beneficiarios/listar_beneficiarios.html', contexto)

@login_required
def cadastrar_beneficiario(request):
    if request.method == 'POST':
        form = FormularioBeneficiario(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Beneficiário cadastrado com sucesso!')
                return redirect('beneficiarios:listar_beneficiarios')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao cadastrar o beneficiário: {e}')
    else:
        form = FormularioBeneficiario()
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Beneficiário'
    }
    return render(request, 'beneficiarios/formulario_beneficiario.html', contexto)

@login_required
def detalhar_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)
    certificados = Certificado.objects.filter(beneficiario=beneficiario).order_by('-data_conclusao', 'curso__nome_curso')
    contexto = {
        'beneficiario': beneficiario,
        'certificados': certificados,
        'titulo_pagina': f'Detalhes de {beneficiario.nome_completo}'
    }
    return render(request, 'beneficiarios/detalhar_beneficiario.html', contexto)

@login_required
def editar_beneficiario(request, beneficiario_id):
    if hasattr(request.user, 'tipo_usuario') and request.user.tipo_usuario == 'VOLUNT':
        messages.error(request, "Você não tem permissão para editar beneficiários.")
        return redirect('beneficiarios:listar_beneficiarios')
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)
    if request.method == 'POST':
        form = FormularioBeneficiario(request.POST, instance=beneficiario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Dados do beneficiário atualizados com sucesso!')
                return redirect('beneficiarios:detalhar_beneficiario', beneficiario_id=beneficiario.id)
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao atualizar o beneficiário: {e}')
    else:
        form = FormularioBeneficiario(instance=beneficiario)
    
    contexto = {
        'form': form,
        'beneficiario': beneficiario,
        'titulo_pagina': f'Editar Beneficiário: {beneficiario.nome_completo}'
    }
    return render(request, 'beneficiarios/formulario_beneficiario.html', contexto)

@login_required
def excluir_beneficiario(request, beneficiario_id): # Inativação
    if hasattr(request.user, 'tipo_usuario') and request.user.tipo_usuario == 'VOLUNT':
        messages.error(request, "Você não tem permissão para inativar beneficiários.")
        return redirect('beneficiarios:listar_beneficiarios')
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)
    if request.method == 'POST':
        try:
            beneficiario.ativo = False
            beneficiario.data_inativacao = timezone.now() # Registrar data de inativação
            beneficiario.save()
            messages.success(request, f'Beneficiário {beneficiario.nome_completo} inativado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao inativar o beneficiário: {e}')
        return redirect('beneficiarios:listar_beneficiarios')
    
    contexto = {
        'beneficiario': beneficiario,
        'titulo_pagina': f'Confirmar Inativação de {beneficiario.nome_completo}'
    }
    return render(request, 'beneficiarios/confirmar_exclusao_beneficiario.html', contexto)

@login_required
def reativar_beneficiario(request, beneficiario_id):
    if hasattr(request.user, 'tipo_usuario') and request.user.tipo_usuario == 'VOLUNT':
        messages.error(request, "Você não tem permissão para reativar beneficiários.")
        # Tenta redirecionar para a página de detalhes do beneficiário se possível, ou lista
        try:
            # Tenta obter o beneficiário para redirecionar para sua página de detalhes
            # Isso pode ser redundante se o ID for sempre válido, mas é uma segurança.
            beneficiario_obj = get_object_or_404(Beneficiario, pk=beneficiario_id)
            return redirect('beneficiarios:detalhar_beneficiario', beneficiario_id=beneficiario_obj.id)
        except:
            return redirect('beneficiarios:listar_beneficiarios')

    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)

    try:
        beneficiario.ativo = True
        beneficiario.data_inativacao = None # Limpar data de inativação
        beneficiario.save()
        messages.success(request, f'Beneficiário {beneficiario.nome_completo} reativado com sucesso.')
    except Exception as e:
        messages.error(request, f'Erro ao reativar o beneficiário: {e}')
    

    return redirect(request.META.get('HTTP_REFERER', 'beneficiarios:listar_beneficiarios'))

@login_required
@admin_required # Apenas admin pode excluir permanentemente
def excluir_permanente_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id, ativo=False) # Só inativos
    if request.method == 'POST':
        try:
            nome_beneficiario = beneficiario.nome_completo
            beneficiario.delete()
            messages.success(request, f'Beneficiário {nome_beneficiario} excluído permanentemente com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao excluir permanentemente o beneficiário: {e}')
        
        redirect_url = reverse('beneficiarios:listar_beneficiarios') + '?filtro_ativo=inativos'
        return redirect(redirect_url)
    
    contexto = {
        'beneficiario': beneficiario,
        'titulo_pagina': f'Confirmar Exclusão Permanente de {beneficiario.nome_completo}'
    }
    return render(request, 'beneficiarios/confirmar_exclusao_permanente_beneficiario.html', contexto)
