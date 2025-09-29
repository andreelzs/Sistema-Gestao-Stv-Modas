from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente
from pedidos.models import Pedido

@login_required
def minha_conta(request):
    cliente = get_object_or_404(Cliente, usuario=request.user)
    pedidos = Pedido.objects.filter(cliente=cliente).order_by('-data_pedido')
    context = {
        'cliente': cliente,
        'pedidos': pedidos
    }
    return render(request, 'clientes/minha_conta.html', context)
