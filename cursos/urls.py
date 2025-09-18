from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('beneficiario/<int:beneficiario_id>/adicionar_certificado/', views.adicionar_certificado_beneficiario, name='adicionar_certificado_beneficiario'),
    path('certificado/<int:certificado_id>/editar/', views.editar_certificado_beneficiario, name='editar_certificado_beneficiario'),
    path('certificado/<int:certificado_id>/excluir/', views.excluir_certificado_beneficiario, name='excluir_certificado_beneficiario'),

    # URLs para Gerenciamento de Cursos da ONG
    path('gerenciar/', views.CursoListView.as_view(), name='listar_cursos_ong'),
    path('gerenciar/novo/', views.CursoCreateView.as_view(), name='criar_curso_ong'),
    path('gerenciar/<int:pk>/editar/', views.CursoUpdateView.as_view(), name='editar_curso_ong'),
    path('gerenciar/<int:pk>/excluir/', views.CursoDeleteView.as_view(), name='excluir_curso_ong'),

    # URL para a aba "Gerar Certificado" (busca de beneficiário)
    # A view CursoListView agora lida com isso, então não precisamos de uma URL separada aqui se a lógica estiver nela.
    # No entanto, se quisermos uma URL dedicada para a aba, mesmo que a view seja a mesma:
    # path('gerar-certificado/', views.CursoListView.as_view(), {'aba_ativa_cursos': 'gerar-certificado'}, name='gerar_certificado_aba'),
    # Por enquanto, a CursoListView já trata a busca de beneficiários e define a aba ativa.

    # URL para a aba "Solicitações de Certificado"
    path('solicitacoes/', views.CertificadoListView.as_view(), name='listar_solicitacoes_certificado'),
]
