import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction

from produtos.models import Categoria, Cor, Tamanho, ProdutoBase, VariacaoProduto
from clientes.models import Cliente, Etiqueta

class Command(BaseCommand):
    help = 'Populates the database with sample data'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting old data...')
        models = [VariacaoProduto, ProdutoBase, Categoria, Cor, Tamanho, Cliente, User, Etiqueta]
        for m in models:
            if m == User:
                m.objects.filter(is_superuser=False).delete()
            else:
                m.objects.all().delete()

        self.stdout.write('Creating new data...')

        # Criar Cores
        cores = [Cor.objects.create(nome=n) for n in ['Preto', 'Branco', 'Vermelho', 'Azul', 'Verde', 'Amarelo']]
        
        # Criar Tamanhos
        tamanhos = [Tamanho.objects.create(nome=n) for n in ['P', 'M', 'G', 'GG']]

        # Criar Categorias
        categorias = [Categoria.objects.create(nome=n) for n in ['Camisetas', 'Calças', 'Vestidos', 'Sapatos']]

        # Criar Produtos Base
        ProdutoBase.objects.create(
            nome='Camiseta Básica', referencia='CB001', categoria=categorias[0], 
            preco_custo=15.00, preco_venda_padrao=49.90
        )
        ProdutoBase.objects.create(
            nome='Calça Jeans Slim', referencia='CJ001', categoria=categorias[1], 
            preco_custo=45.00, preco_venda_padrao=129.90
        )
        ProdutoBase.objects.create(
            nome='Vestido Floral', referencia='VF001', categoria=categorias[2], 
            preco_custo=30.00, preco_venda_padrao=99.90
        )

        # Criar Variações de Produto
        for produto in ProdutoBase.objects.all():
            for cor in random.sample(cores, k=random.randint(2, 4)):
                for tamanho in random.sample(tamanhos, k=random.randint(2, 4)):
                    VariacaoProduto.objects.create(
                        produto_base=produto,
                        cor=cor,
                        tamanho=tamanho,
                        estoque=random.randint(5, 50)
                    )

        # Criar Etiquetas
        etiquetas = [Etiqueta.objects.create(nome=n) for n in ['VIP', 'Novo Cliente', 'Bom Pagador', 'Inativo']]

        # Criar Clientes
        for i in range(10):
            username = f'cliente{i+1}'
            user, created = User.objects.get_or_create(username=username, defaults={'first_name': f'Cliente {i+1}', 'last_name': 'Sobrenome'})
            if created:
                user.set_password('123456')
                user.save()
            
            cliente, _ = Cliente.objects.get_or_create(
                usuario=user,
                defaults={
                    'nome_completo': f'Cliente {i+1} Sobrenome Fictício',
                    'telefone': f'99999-99{i:02d}',
                    'logradouro': f'Rua das Flores, {i+1}',
                    'numero': f'{i+1}0',
                    'bairro': 'Centro',
                    'cidade': 'Cidade Fictícia',
                    'cep': f'12345-0{i:02d}'
                }
            )
            cliente.etiquetas.add(random.choice(etiquetas))
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))
