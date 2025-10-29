from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard_view'),
    path('produtos/', views.lista_produtos, name='lista_produtos'),
    path('produtos/add/', views.add_produto, name='add_produto'),
    path('produtos/edit/<int:pk>/', views.edit_produto, name='edit_produto'),
    path('produtos/delete/<int:pk>/', views.delete_produto, name='delete_produto'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/add/', views.add_cliente, name='add_cliente'),
    path('clientes/edit/<int:pk>/', views.edit_cliente, name='edit_cliente'),
    path('clientes/delete/<int:pk>/', views.delete_cliente, name='delete_cliente'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
]
