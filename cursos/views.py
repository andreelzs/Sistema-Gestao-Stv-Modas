from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Certificado, Curso
from beneficiarios.models import Beneficiario
from .forms import CertificadoForm, CursoForm # Adicionado CursoForm
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Adicionado para paginação
@login_required
def adicionar_certificado_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        if form.is_valid():
            certificado = form.save(commit=False)
            certificado.beneficiario = beneficiario
            certificado.save()
            form.save_m2m() # Garantir que M2M (se houver no CertificadoForm no futuro) seja salvo
            messages.success(request, f"Certificado do curso '{certificado.curso.nome_curso}' adicionado para {beneficiario.nome_completo}.")
            return redirect('cursos:listar_solicitacoes_certificado') # Redirecionamento alterado
        else:
            messages.error(request, "Erro ao adicionar o certificado. Verifique os dados informados.")
    else:
        form = CertificadoForm()

    context = {
        'form': form,
        'beneficiario': beneficiario,
        'titulo_pagina': f"Adicionar Certificado para {beneficiario.nome_completo}"
    }
    return render(request, 'cursos/formulario_certificado.html', context)

@login_required
def editar_certificado_beneficiario(request, certificado_id):
    certificado = get_object_or_404(Certificado, pk=certificado_id)
    beneficiario = certificado.beneficiario
    if request.method == 'POST':
        form = CertificadoForm(request.POST, instance=certificado)
        if form.is_valid():
            form.save() # ModelForm.save() já lida com M2M se commit=True (padrão)
            messages.success(request, f"Certificado do curso '{certificado.curso.nome_curso}' atualizado para {beneficiario.nome_completo}.")
            return redirect('cursos:listar_solicitacoes_certificado') # Redirecionamento alterado
        else:
            messages.error(request, "Erro ao atualizar o certificado. Verifique os dados informados.")
    else:
        form = CertificadoForm(instance=certificado)

    context = {
        'form': form,
        'beneficiario': beneficiario,
        'certificado': certificado,
        'titulo_pagina': f"Editar Certificado de {beneficiario.nome_completo}"
    }
    return render(request, 'cursos/formulario_certificado.html', context)

@login_required
def excluir_certificado_beneficiario(request, certificado_id):
    certificado = get_object_or_404(Certificado, pk=certificado_id)
    beneficiario_id = certificado.beneficiario.id
    nome_curso = certificado.curso.nome_curso
    nome_beneficiario = certificado.beneficiario.nome_completo

    if request.method == 'POST':
        certificado.delete()
        messages.success(request, f"Certificado do curso '{nome_curso}' para {nome_beneficiario} foi excluído.")
        return redirect('cursos:listar_solicitacoes_certificado')

    context = {
        'certificado': certificado,
        'beneficiario': certificado.beneficiario,
        'titulo_pagina': "Confirmar Exclusão de Certificado"
    }
    return render(request, 'cursos/confirmar_exclusao_certificado.html', context)


# Views para Gerenciamento de Cursos da ONG

class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'cursos/curso_list.html' # Especificar o nome do template
    context_object_name = 'cursos'
    paginate_by = 10 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Dados para a primeira aba (Gerenciar Tipos de Curso) já são tratados por ListView para 'cursos'
        context['titulo_pagina_aba_gerenciar'] = "Tipos de Curso Oferecidos" # Título específico para o conteúdo da aba

        # Dados para a segunda aba (Gerar Certificado - Busca de Beneficiário)
        termo_pesquisa_beneficiario = self.request.GET.get('q_beneficiario', None)
        beneficiarios_list = Beneficiario.objects.filter(ativo=True)
        if termo_pesquisa_beneficiario:
            beneficiarios_list = beneficiarios_list.filter(nome_completo__icontains=termo_pesquisa_beneficiario)
        
        paginator_beneficiarios = Paginator(beneficiarios_list.order_by('nome_completo'), 10) # 10 beneficiários por página
        page_number_beneficiarios = self.request.GET.get('page_beneficiarios') # Usar um param de página diferente
        try:
            context['page_obj_beneficiarios'] = paginator_beneficiarios.page(page_number_beneficiarios)
        except PageNotAnInteger:
            context['page_obj_beneficiarios'] = paginator_beneficiarios.page(1)
        except EmptyPage:
            context['page_obj_beneficiarios'] = paginator_beneficiarios.page(paginator_beneficiarios.num_pages)
        
        context['termo_pesquisa_beneficiario_atual'] = termo_pesquisa_beneficiario
        context['titulo_pagina_aba_gerar_certificado'] = "Gerar Certificado - Buscar Beneficiário"

        # Placeholder para dados da terceira aba (Solicitações de Certificado)
        
        # Determinar aba ativa para o template curso_list.html
        param_aba_ativa = self.request.GET.get('aba_ativa_cursos')
        if param_aba_ativa == 'gerar-certificado' or termo_pesquisa_beneficiario is not None:
            context['aba_ativa_cursos'] = 'gerar-certificado'
        else:
            context['aba_ativa_cursos'] = 'gerenciar-tipos-curso' # Default para esta view


        return context

class CursoCreateView(LoginRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html' # Template para criar e atualizar
    success_url = reverse_lazy('cursos:listar_cursos_ong') # Nome da URL para a lista de cursos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = "Adicionar Novo Curso"
        context['texto_botao'] = "Salvar Novo Curso"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Curso adicionado com sucesso!")
        return super().form_valid(form)

class CursoUpdateView(LoginRequiredMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    success_url = reverse_lazy('cursos:listar_cursos_ong')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f"Editar Curso: {self.object.nome_curso}"
        context['texto_botao'] = "Salvar Alterações"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Curso atualizado com sucesso!")
        return super().form_valid(form)

class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'cursos/curso_confirm_delete.html' # Template para confirmar exclusão
    success_url = reverse_lazy('cursos:listar_cursos_ong')
    context_object_name = 'curso' # Para usar {{ curso }} no template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f"Confirmar Exclusão do Curso: {self.object.nome_curso}"
        return context
    
    def post(self, request, *args, **kwargs):
        
        curso_nome = self.get_object().nome_curso
        # Verificar se há certificados associados antes de excluir
        if Certificado.objects.filter(curso=self.get_object()).exists():
            messages.error(request, f"Não é possível excluir o curso '{curso_nome}', pois existem certificados associados a ele. Remova os certificados primeiro.")
            return redirect(self.success_url) # Ou para a página de detalhes do curso, se houver

        messages.success(request, f"Curso '{curso_nome}' excluído com sucesso.")
        return super().delete(request, *args, **kwargs) # Chama o método delete padrão


class BuscarBeneficiarioParaCertificadoView(LoginRequiredMixin, ListView):
    model = Beneficiario
    template_name = 'cursos/buscar_beneficiario_para_certificado.html'
    context_object_name = 'beneficiarios'
    paginate_by = 10

    def get_queryset(self):
        queryset = Beneficiario.objects.filter(ativo=True) # Começa com beneficiários ativos
        termo_pesquisa = self.request.GET.get('q_beneficiario', None)
        if termo_pesquisa:
            queryset = queryset.filter(nome_completo__icontains=termo_pesquisa)
        return queryset.order_by('nome_completo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = "Gerar Certificado - Buscar Beneficiário"
        context['termo_pesquisa_atual'] = self.request.GET.get('q_beneficiario', '')
        # Passa a URL da aba atual para manter a aba ativa após a busca
        context['aba_ativa'] = 'gerar-certificado' 
        return context


class CertificadoListView(LoginRequiredMixin, ListView):
    model = Certificado
    template_name = 'cursos/solicitacoes_certificado_list.html' # Novo template para esta lista
    context_object_name = 'certificados'
    paginate_by = 15

    def get_queryset(self):
        queryset = Certificado.objects.select_related('beneficiario', 'curso').all()
        
        # Filtros
        filtro_curso = self.request.GET.get('filtro_curso')
        filtro_beneficiario = self.request.GET.get('filtro_beneficiario_nome')
        filtro_recebido = self.request.GET.get('filtro_recebido')

        if filtro_curso:
            queryset = queryset.filter(curso__id=filtro_curso)
        if filtro_beneficiario:
            queryset = queryset.filter(beneficiario__nome_completo__icontains=filtro_beneficiario)
        if filtro_recebido is not None and filtro_recebido != '':
            queryset = queryset.filter(certificado_recebido=(filtro_recebido == 'true'))

        # Ordenação
        ordenar_por_data_conclusao = self.request.GET.get('ordenar_por_data_conclusao')
        ordenar_por_data_emissao = self.request.GET.get('ordenar_por_data_emissao')

        if ordenar_por_data_conclusao:
            if ordenar_por_data_conclusao == 'asc':
                queryset = queryset.order_by('data_conclusao', 'beneficiario__nome_completo')
            elif ordenar_por_data_conclusao == 'desc':
                queryset = queryset.order_by('-data_conclusao', 'beneficiario__nome_completo')
        elif ordenar_por_data_emissao:
            if ordenar_por_data_emissao == 'asc':
                queryset = queryset.order_by('data_emissao_certificado', 'beneficiario__nome_completo')
            elif ordenar_por_data_emissao == 'desc':
                queryset = queryset.order_by('-data_emissao_certificado', 'beneficiario__nome_completo')
        else:
            # Ordenação padrão
            queryset = queryset.order_by('-data_conclusao', 'beneficiario__nome_completo')
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = "Solicitações de Certificado"
        context['cursos_disponiveis'] = Curso.objects.all().order_by('nome_curso') # Para o filtro
        
        # Manter os valores dos filtros para preencher o formulário de filtro
        context['filtro_curso_atual'] = self.request.GET.get('filtro_curso', '')
        context['filtro_beneficiario_nome_atual'] = self.request.GET.get('filtro_beneficiario_nome', '')
        context['filtro_recebido_atual'] = self.request.GET.get('filtro_recebido', '')

        # Parâmetros de ordenação para o contexto
        context['ordenacao_data_conclusao_atual'] = self.request.GET.get('ordenar_por_data_conclusao')
        context['ordenacao_data_emissao_atual'] = self.request.GET.get('ordenar_por_data_emissao')
        
        # Para a navegação por abas
        context['aba_ativa_cursos'] = 'solicitacoes-certificado' 
        return context
