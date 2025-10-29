from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('minha-conta/', views.minha_conta, name='minha_conta'),
]
