# Dentro do ficheiro: produtos/views.py

from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import ProdutoBase
from .forms import ProdutoBaseForm

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
        return context
