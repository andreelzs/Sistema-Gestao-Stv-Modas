# Dentro do ficheiro: produtos/views.py

from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from .models import ProdutoBase, Cor, Marca, Categoria
from .forms import ProdutoBaseForm, VariacaoProdutoFormSet, ImagemProdutoFormSet

class ProdutoListView(LoginRequiredMixin, ListView):
    """
    View para listar todos os produtos que estão ativos.
    Apenas utilizadores logados (administradores) podem aceder.
    """
    model = ProdutoBase
    template_name = 'produtos/listar_produtos.html'
    context_object_name = 'produtos'
    paginate_by = 10  # Mostra 10 produtos por página para não sobrecarregar a tela

    def get_queryset(self):
        """
        Sobrescrevemos o método padrão get_queryset.
        Esta é a parte crucial que implementa a sua ideia de "arquivamento".
        Em vez de retornar ProdutoBase.objects.all(), nós filtramos
        para retornar apenas os produtos onde o campo 'ativo' é True.
        """
        queryset = super().get_queryset().filter(ativo=True)
        return queryset.order_by('nome')
    
class ProdutoCreateView(LoginRequiredMixin, CreateView):
    """
    View para a página de formulário de criação de um novo produto.
    """
    model = ProdutoBase
    form_class = ProdutoBaseForm
    template_name = 'produtos/adicionar_produto.html'
    # Após o sucesso da criação, redireciona para a lista de produtos
    success_url = reverse_lazy('produtos:listar_produtos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Produto"
        
        # Adicionar formsets ao contexto se não estiverem no POST
        if self.request.POST:
            context['variacoes_formset'] = VariacaoProdutoFormSet(self.request.POST, self.request.FILES, instance=self.object)
            context['imagens_formset'] = ImagemProdutoFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['variacoes_formset'] = VariacaoProdutoFormSet(instance=self.object)
            context['imagens_formset'] = ImagemProdutoFormSet(instance=self.object)
            
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        variacoes_formset = context['variacoes_formset']
        imagens_formset = context['imagens_formset']
        
        # Verificar se os formsets são válidos
        if variacoes_formset.is_valid() and imagens_formset.is_valid():
            # Salvar o produto base
            self.object = form.save()
            
            # Salvar as variações
            variacoes_formset.instance = self.object
            variacoes_formset.save()
            
            # Salvar as imagens
            imagens_formset.instance = self.object
            imagens_formset.save()
            
            return super().form_valid(form)
        else:
            # Se algum formset não é válido, retornar ao formulário com erros
            return self.render_to_response(self.get_context_data(form=form))

@csrf_exempt
def adicionar_cor_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome_cor = data.get('nome')
            
            # Verificar se a cor já existe
            cor, created = Cor.objects.get_or_create(nome=nome_cor)
            
            if created:
                return JsonResponse({
                    'success': True,
                    'id': cor.id,
                    'nome': cor.nome
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Cor já existe'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'Método não permitido'
    })

@csrf_exempt
def adicionar_marca_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome_marca = data.get('nome')

            # Verificar se a marca já existe
            marca, created = Marca.objects.get_or_create(nome=nome_marca)

            if created:
                return JsonResponse({
                    'success': True,
                    'id': marca.id,
                    'nome': marca.nome
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Marca já existe'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'Método não permitido'
    })

@csrf_exempt
def adicionar_categoria_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome_categoria = data.get('nome')

            # Verificar se a categoria já existe
            categoria, created = Categoria.objects.get_or_create(nome=nome_categoria)

            if created:
                return JsonResponse({
                    'success': True,
                    'id': categoria.id,
                    'nome': categoria.nome
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Categoria já existe'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'Método não permitido'
    })

@csrf_exempt
def adicionar_tamanho_ajax(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome_tamanho = data.get('nome')

            # Verificar se o tamanho já existe
            tamanho, created = Tamanho.objects.get_or_create(nome=nome_tamanho)

            if created:
                return JsonResponse({
                    'success': True,
                    'id': tamanho.id,
                    'nome': tamanho.nome
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Tamanho já existe'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    return JsonResponse({
        'success': False,
        'error': 'Método não permitido'
    })
