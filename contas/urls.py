from django.urls import path
from . import views # Importaremos as views deste app
# Se for usar as views de autenticação padrão do Django:
# from django.contrib.auth import views as auth_views

app_name = 'contas'

from .views import LoginUsuarioView, LogoutUsuarioView # Importar as views que criamos

urlpatterns = [
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutUsuarioView.as_view(), name='logout'),
    # Futuramente:
    # path('cadastro/', views.cadastro_usuario_view, name='cadastro_usuario'),
]
