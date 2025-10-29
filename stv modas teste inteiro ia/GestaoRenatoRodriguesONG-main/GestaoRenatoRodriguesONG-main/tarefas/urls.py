from django.urls import path
from . import views

app_name = 'tarefas'

urlpatterns = [
    path('', views.listar_tarefas, name='listar_tarefas'),
    path('nova/', views.cadastrar_tarefa, name='cadastrar_tarefa'),
    path('<int:tarefa_id>/', views.detalhar_tarefa, name='detalhar_tarefa'),
    path('<int:tarefa_id>/editar/', views.editar_tarefa, name='editar_tarefa'),
    path('<int:tarefa_id>/excluir/', views.excluir_tarefa, name='excluir_tarefa'),
    path('<int:tarefa_id>/atualizar_status/<str:novo_status>/', views.atualizar_status_tarefa, name='atualizar_status_tarefa'),
]
