"""
URL configuration for gestao_stv_modas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from produtos import views

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name='listar_produtos'),
    path('admin/', admin.site.urls),
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),
    path('', include('core.urls', namespace='core')), # Incluir as URLs do app core
    path('contas/', include('contas.urls', namespace='contas')), # Incluir as URLs do app contas
    path('clientes/', include('clientes.urls', namespace='clientes')), # Incluir as URLs do app clientes
    path('dashboard/', include('dashboard.urls', namespace='dashboard')), # Incluir as URLs do app dashboard
    path('produtos/', include('produtos.urls')), # Incluir as URLs do app produtos
    path('adicionar/', views.ProdutoCreateView.as_view(), name='adicionar_produto') # Incluir as URLs do app produtos
]
