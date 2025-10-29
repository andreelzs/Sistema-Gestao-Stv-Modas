from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from pedidos.models import Pedido
from clientes.models import Cliente
from produtos.models import ProdutoBase, Categoria, Cor, Tamanho, VariacaoProduto
from django.contrib import messages
from django.db.models import F
from django.forms import inlineformset_factory
from produtos.forms import ProdutoBaseForm, VariacaoProdutoForm, ImagemProdutoForm # Precisaremos criar esses forms

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def dashboard_view(request):
    # Exemplo de dados para o dashboard
    total_pedidos = Pedido.objects.count()
    pedidos_pendentes = Pedido.objects.filter(status='AGUARDANDO_PAGAMENTO').count()
    total_clientes = Cliente.objects.count()
    total_produtos = ProdutoBase.objects.count()

    context = {
        'total_pedidos': total_pedidos,
        'pedidos_pendentes': pedidos_pendentes,
        'total_clientes': total_clientes,
        'total_produtos': total_produtos,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
@user_passes_test(is_staff)
def lista_produtos(request):
    produtos = ProdutoBase.objects.all().order_by('nome')
    context = {
        'produtos': produtos
    }
    return render(request, 'dashboard/produtos/lista.html', context)

@login_required
@user_passes_test(is_staff)
def add_produto(request):
    # Lógica para adicionar produto
    return render(request, 'dashboard/produtos/form.html', {})

@login_required
@user_passes_test(is_staff)
def edit_produto(request, pk):
    # Lógica para editar produto
    return render(request, 'dashboard/produtos/form.html', {})

@login_required
@user_passes_test(is_staff)
def delete_produto(request, pk):
    # Lógica para deletar produto
    return redirect('dashboard:lista_produtos')

@login_required
@user_passes_test(is_staff)
def add_cliente(request):
    # Lógica para adicionar cliente
    return render(request, 'dashboard/clientes/form.html', {})

@login_required
@user_passes_test(is_staff)
def edit_cliente(request, pk):
    # Lógica para editar cliente
    return render(request, 'dashboard/clientes/form.html', {})

@login_required
@user_passes_test(is_staff)
def delete_cliente(request, pk):
    # Lógica para deletar cliente
    return redirect('dashboard:lista_clientes')

@login_required
@user_passes_test(is_staff)
def add_pedido(request):
    # Lógica para adicionar pedido
    return render(request, 'dashboard/pedidos/form.html', {})

@login_required
@user_passes_test(is_staff)
def edit_pedido(request, pk):
    # Lógica para editar pedido
    return render(request, 'dashboard/pedidos/form.html', {})

@login_required
@user_passes_test(is_staff)
def delete_pedido(request, pk):
    # Lógica para deletar pedido
    return redirect('dashboard:lista_pedidos')

@login_required
@user_passes_test(is_staff)
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('nome_completo')
    context = {
        'clientes': clientes
    }
    return render(request, 'dashboard/clientes/lista.html', context)

@login_required
@user_passes_test(is_staff)
def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-data_pedido')
    context = {
        'pedidos': pedidos
    }
    return render(request, 'dashboard/pedidos/lista.html', context)
