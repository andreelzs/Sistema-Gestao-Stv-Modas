
from django.http import JsonResponse
from .models import ProdutoBase

def buscar_variacoes(request):
    produto_id = request.GET.get('produto_id')
    try:
        produto = ProdutoBase.objects.get(id=produto_id)
        variacoes = produto.variacoes.all()
        
        # Estrutura de dados para o JavaScript
        cores = {}
        for var in variacoes:
            cor_id = var.cor.id if var.cor else None
            cor_nome = var.cor.nome if var.cor else 'N/A'
            tamanho_id = var.tamanho.id if var.tamanho else None
            tamanho_nome = var.tamanho.nome if var.tamanho else 'N/A'

            if cor_id not in cores:
                cores[cor_id] = {'nome': cor_nome, 'tamanhos': []}
            
            cores[cor_id]['tamanhos'].append({
                'id': tamanho_id,
                'nome': tamanho_nome,
                'variacao_id': var.id,
                'estoque': var.estoque,
                'preco': var.get_preco_venda
            })
            
        return JsonResponse({'cores': cores})
    except ProdutoBase.DoesNotExist:
        return JsonResponse({'error': 'Produto não encontrado'}, status=404)