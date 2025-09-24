from django.urls import path
from . import views

app_name = 'voluntarios'

urlpatterns = [
    path('', views.listar_voluntarios, name='listar_voluntarios'),
    path('novo/', views.cadastrar_voluntario, name='cadastrar_voluntario'),
    path('<int:voluntario_id>/', views.detalhar_voluntario, name='detalhar_voluntario'),
    path('<int:voluntario_id>/editar/', views.editar_voluntario, name='editar_voluntario'),
    path('<int:voluntario_id>/excluir/', views.excluir_voluntario, name='excluir_voluntario'), # Inativar
    path('<int:voluntario_id>/reativar/', views.reativar_voluntario, name='reativar_voluntario'),
    path('<int:voluntario_id>/excluir-permanente/', views.excluir_permanente_voluntario, name='excluir_permanente_voluntario'),
]
