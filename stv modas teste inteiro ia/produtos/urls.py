# Dentro do ficheiro: produtos/urls.py

from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # URL para a nossa nova página de listagem de produtos.
    # O caminho vazio ('') significa que esta será a página principal do app de produtos.
    # Ex: http://127.0.0.1:8000/produtos/
    path('', views.ProdutoListView.as_view(), name='listar_produtos'),

    # URL para adicionar um novo produto.
    path('adicionar/', views.ProdutoCreateView.as_view(), name='adicionar_produto'),
    
    # URLs para adicionar cor, marca e categoria via AJAX
    path('adicionar-cor-ajax/', views.adicionar_cor_ajax, name='adicionar_cor_ajax'),
    path('adicionar-marca-ajax/', views.adicionar_marca_ajax, name='adicionar_marca_ajax'),
    path('adicionar-categoria-ajax/', views.adicionar_categoria_ajax, name='adicionar_categoria_ajax'),

    # Futuramente, adicionaremos as URLs para editar e arquivar produtos aqui.
]
