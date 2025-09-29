from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('api/get-cores-disponiveis/', views.get_cores_disponiveis, name='get_cores_disponiveis'),
    path('api/get-tamanhos-disponiveis/', views.get_tamanhos_disponiveis, name='get_tamanhos_disponiveis'),
    path('api/get-variacao-completa/', views.get_variacao_completa, name='get_variacao_completa'),
    path('<int:pedido_id>/', views.detalhe_pedido, name='detalhe_pedido'), # URL para detalhe do pedido
]
