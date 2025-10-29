from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from produtos.models import ProdutoBase, Cor, Tamanho, VariacaoProduto
from .models import Pedido, ItemPedido, Parcela
from clientes.models import Cliente

def get_cores_disponiveis(request):
    produto_base_id = request.GET.get('produto_base_id')
    if not produto_base_id:
        return JsonResponse({'error': 'ID do Produto Base não fornecido'}, status=400)
    
    variacoes = VariacaoProduto.objects.filter(produto_base_id=produto_base_id, estoque__gt=0)
    cores_ids = variacoes.values_list('cor__id', flat=True).distinct()
    cores = Cor.objects.filter(id__in=cores_ids).values('id', 'nome')
    return JsonResponse({'cores': list(cores)})

def get_tamanhos_disponiveis(request):
    produto_base_id = request.GET.get('produto_base_id')
    cor_id = request.GET.get('cor_id')
    
    if not produto_base_id or not cor_id:
        return JsonResponse({'error': 'ID do Produto Base e/ou Cor não fornecidos'}, status=400)
        
    variacoes = VariacaoProduto.objects.filter(
        produto_base_id=produto_base_id,
        cor_id=cor_id,
        estoque__gt=0
    )
    tamanhos_ids = variacoes.values_list('tamanho__id', flat=True).distinct()
    tamanhos = Tamanho.objects.filter(id__in=tamanhos_ids).values('id', 'nome')
    return JsonResponse({'tamanhos': list(tamanhos)})

def get_variacao_completa(request):
    produto_base_id = request.GET.get('produto_base_id')
    cor_id = request.GET.get('cor_id')
    tamanho_id = request.GET.get('tamanho_id')

    if not produto_base_id or not cor_id or not tamanho_id:
        return JsonResponse({'error': 'IDs de Produto Base, Cor e/ou Tamanho não fornecidos'}, status=400)
    
    variacao = get_object_or_404(
        VariacaoProduto,
        produto_base_id=produto_base_id,
        cor_id=cor_id,
        tamanho_id=tamanho_id,
        estoque__gt=0
    )
    
    data = {
        'id': variacao.id,
        'preco': variacao.get_preco_venda,
        'estoque': variacao.estoque,
    }
    return JsonResponse(data)

@login_required
def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente__usuario=request.user)
    itens_pedido = ItemPedido.objects.filter(pedido=pedido)
    parcelas = Parcela.objects.filter(pedido=pedido).order_by('numero_parcela')

    context = {
        'pedido': pedido,
        'itens_pedido': itens_pedido,
        'parcelas': parcelas,
    }
    return render(request, 'pedidos/detalhe_pedido.html', context)
