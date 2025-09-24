"""
URL configuration for gerenciamento_ong project.

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
from django.urls import path, include # Adicionar include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('contas/', include('contas.urls', namespace='contas')),
    path('voluntarios/', include('voluntarios.urls', namespace='voluntarios')),
    path('beneficiarios/', include('beneficiarios.urls', namespace='beneficiarios')),
    path('tarefas/', include('tarefas.urls', namespace='tarefas')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('cursos/', include('cursos.urls', namespace='cursos')), # URLs do app cursos
]
