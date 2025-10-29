from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Para proteger views
from django.utils import timezone # Adicionado para data_inativacao
from django.urls import reverse # Adicionado para construir URL com query string
from .models import Voluntario
from .forms import FormularioVoluntario
from contas.decorators import admin_required # Importar o decorator

@login_required
def listar_voluntarios(request):
    filtro_ativo_param = request.GET.get('filtro_ativo', 'ativos')

    if filtro_ativo_param == 'inativos':
        voluntarios = Voluntario.objects.filter(ativo=False).order_by('nome_completo')
        titulo_pagina_especifico = 'Voluntários Inativos'
    else: # 'ativos' ou qualquer outro valor
        voluntarios = Voluntario.objects.filter(ativo=True).order_by('nome_completo')
        titulo_pagina_especifico = 'Voluntários Ativos'
        filtro_ativo_param = 'ativos' # Garante que o valor seja 'ativos' se não for 'inativos'

    contexto = {
        'voluntarios': voluntarios,
        'titulo_pagina': titulo_pagina_especifico,
        'filtro_ativo_atual': filtro_ativo_param
    }
    return render(request, 'voluntarios/listar_voluntarios.html', contexto)

@login_required
@admin_required # Restringir cadastro a admins
def cadastrar_voluntario(request):
    if request.method == 'POST':
        form = FormularioVoluntario(request.POST, user=request.user) # Passar user
        if form.is_valid():
            try:
                form.save() 
                messages.success(request, 'Voluntário cadastrado com sucesso!')
                return redirect('voluntarios:listar_voluntarios')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao cadastrar o voluntário: {e}')
        else:
            # Se o formulário não for válido, exibe mensagens de erro já tratadas no formulário
            pass 
    else:
        form = FormularioVoluntario(user=request.user) # Passar user
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Voluntário'
    }
    return render(request, 'voluntarios/formulario_voluntario.html', contexto)

# Views para Detalhar, Editar e Excluir
@login_required
def detalhar_voluntario(request, voluntario_id):
    voluntario = get_object_or_404(Voluntario, pk=voluntario_id)
    contexto = {
        'voluntario': voluntario,
        'titulo_pagina': f'Detalhes de {voluntario.nome_completo}'
    }
    return render(request, 'voluntarios/detalhar_voluntario.html', contexto)

@login_required
def editar_voluntario(request, voluntario_id):
    voluntario = get_object_or_404(Voluntario, pk=voluntario_id)
    
    # Restrição: Voluntário só pode editar o próprio perfil.
    # Admins podem editar qualquer um.
    if hasattr(request.user, 'tipo_usuario') and request.user.tipo_usuario == 'VOLUNT':
        # Verifica se o voluntário logado é o mesmo que está sendo editado
        if not (hasattr(voluntario, 'usuario') and voluntario.usuario == request.user):
            messages.error(request, "Você só tem permissão para editar seu próprio perfil.")
            # Tenta redirecionar para o perfil do próprio usuário logado, se ele tiver um.
            # Caso contrário, para a lista de voluntários.
            if hasattr(request.user, 'voluntario') and request.user.voluntario:
                 return redirect('voluntarios:detalhar_voluntario', voluntario_id=request.user.voluntario.id)
            else:
                 return redirect('voluntarios:listar_voluntarios')


    if request.method == 'POST':
        form = FormularioVoluntario(request.POST, instance=voluntario, user=request.user) # Passar user
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Dados do voluntário atualizados com sucesso!')
                return redirect('voluntarios:detalhar_voluntario', voluntario_id=voluntario.id)
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao atualizar o voluntário: {e}')
    else:
        form = FormularioVoluntario(instance=voluntario, user=request.user) # Passar user
        # Se o voluntário tem um usuário associado, preenche os campos de usuário no formulário

    contexto = {
        'form': form,
        'voluntario': voluntario,
        'titulo_pagina': f'Editar Voluntário: {voluntario.nome_completo}'
    }
    return render(request, 'voluntarios/formulario_voluntario.html', contexto)

@login_required
@admin_required # Apenas admin pode inativar outros voluntários
def excluir_voluntario(request, voluntario_id):
    # Um admin não deve poder inativar a si mesmo através desta view
    # (se o voluntario.usuario for o request.user, impedir ou tratar de forma especial)
    # Esta verificação pode ser adicionada se necessário.
    voluntario = get_object_or_404(Voluntario, pk=voluntario_id)
    if request.method == 'POST':
        try:
            # Em vez de excluir, podemos apenas inativar o voluntário e seu usuário
            voluntario.ativo = False
            voluntario.data_inativacao = timezone.now() # Registrar data de inativação
            if hasattr(voluntario, 'usuario') and voluntario.usuario:
                voluntario.usuario.is_active = False
                voluntario.usuario.save()
            voluntario.save()
            messages.success(request, f'Voluntário {voluntario.nome_completo} inativado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao inativar o voluntário: {e}')
        return redirect('voluntarios:listar_voluntarios')
    
    contexto = {
        'voluntario': voluntario,
        'titulo_pagina': f'Confirmar Inativação de {voluntario.nome_completo}'
    }
    return render(request, 'voluntarios/confirmar_exclusao_voluntario.html', contexto)

@login_required
def reativar_voluntario(request, voluntario_id):
    voluntario = get_object_or_404(Voluntario, pk=voluntario_id)
    if request.method == 'POST': # Geralmente a reativação é uma ação POST para evitar CSRF com links diretos
        try:
            voluntario.ativo = True
            voluntario.data_inativacao = None # Limpar data de inativação
            if hasattr(voluntario, 'usuario') and voluntario.usuario:
                voluntario.usuario.is_active = True
                voluntario.usuario.save()
            voluntario.save()
            messages.success(request, f'Voluntário {voluntario.nome_completo} reativado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao reativar o voluntário: {e}')
        # Redireciona para a lista de inativos para ver que ele sumiu de lá, 
        # ou para a lista de ativos para vê-lo lá.
        return redirect('voluntarios:listar_voluntarios') # Por padrão, vai para ativos. Pode adicionar ?filtro_ativo=inativos se preferir
    
    try:
        voluntario.ativo = True
        voluntario.data_inativacao = None
        if hasattr(voluntario, 'usuario') and voluntario.usuario:
            voluntario.usuario.is_active = True
            voluntario.usuario.save()
        voluntario.save()
        messages.success(request, f'Voluntário {voluntario.nome_completo} reativado com sucesso.')
    except Exception as e:
        messages.error(request, f'Erro ao reativar o voluntário: {e}')
    return redirect(request.META.get('HTTP_REFERER', 'voluntarios:listar_voluntarios'))

@login_required
@admin_required # Apenas admin pode excluir permanentemente
def excluir_permanente_voluntario(request, voluntario_id):
    voluntario = get_object_or_404(Voluntario, pk=voluntario_id, ativo=False) # Garante que só inativos podem ser excluídos permanentemente
    if request.method == 'POST':
        try:
            nome_voluntario = voluntario.nome_completo
            # O OneToOneField com usuario tem on_delete=models.CASCADE, 
            # então o usuário associado será excluído automaticamente.
            voluntario.delete()
            messages.success(request, f'Voluntário {nome_voluntario} excluído permanentemente com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao excluir permanentemente o voluntário: {e}')
        
        redirect_url = reverse('voluntarios:listar_voluntarios') + '?filtro_ativo=inativos'
        return redirect(redirect_url) # Volta para a lista de inativos
    
    contexto = {
        'voluntario': voluntario,
        'titulo_pagina': f'Confirmar Exclusão Permanente de {voluntario.nome_completo}'
    }
    return render(request, 'voluntarios/confirmar_exclusao_permanente_voluntario.html', contexto)
