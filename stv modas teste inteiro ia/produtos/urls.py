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

    # Futuramente, adicionaremos as URLs para editar e arquivar produtos aqui.
]
