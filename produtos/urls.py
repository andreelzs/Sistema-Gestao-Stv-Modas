from django.urls import path
from . import views

app_name = 'beneficiarios'

urlpatterns = [
    path('', views.listar_beneficiarios, name='listar_beneficiarios'),
    path('novo/', views.cadastrar_beneficiario, name='cadastrar_beneficiario'),
    path('<int:beneficiario_id>/', views.detalhar_beneficiario, name='detalhar_beneficiario'),
    path('<int:beneficiario_id>/editar/', views.editar_beneficiario, name='editar_beneficiario'),
    path('<int:beneficiario_id>/excluir/', views.excluir_beneficiario, name='excluir_beneficiario'), # Inativar
    path('<int:beneficiario_id>/reativar/', views.reativar_beneficiario, name='reativar_beneficiario'),
    path('<int:beneficiario_id>/excluir-permanente/', views.excluir_permanente_beneficiario, name='excluir_permanente_beneficiario'),
]
