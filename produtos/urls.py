# Dentro do ficheiro: produtos/urls.py

from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    # Nova URL para a nossa API interna
    path('api/buscar-variacoes/', views.buscar_variacoes, name='buscar_variacoes'),
]