from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def painel_principal(request):
    # Futuramente, vamos buscar dados de Pedidos, Clientes e Produtos
    # para exibir no dashboard.
    contexto = {
        'titulo': 'Dashboard'
    }
    return render(request, 'dashboard/painel_principal.html', contexto)