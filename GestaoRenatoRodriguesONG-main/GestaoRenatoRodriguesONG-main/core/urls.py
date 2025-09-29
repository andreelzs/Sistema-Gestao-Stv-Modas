from django.urls import path
from . import views # Importaremos as views deste app

app_name = 'core'

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
]
