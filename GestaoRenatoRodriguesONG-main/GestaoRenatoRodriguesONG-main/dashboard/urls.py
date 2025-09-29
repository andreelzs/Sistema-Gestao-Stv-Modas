from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.painel_principal, name='painel_principal'),
    # Outras URLs para gráficos específicos ou dados de API podem ser adicionadas aqui depois
]
