from django.db import models
from django.utils import timezone
from clientes.models import Cliente
from produtos.models import VariacaoProduto

class Pedido(models.Model):
    FORMAS_PAGAMENTO = [
        ('PIX', 'PIX'),
        ('CARTAO', 'Cartão de Crédito'),
        ('CREDIARIO', 'Crediário'),
    ]
    STATUS_PEDIDO = [
        ('AGUARDANDO_PAGAMENTO', 'Aguardando Pagamento'),
        ('EM_SEPARACAO', 'Em Separação'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    forma_pagamento = models.CharField(max_length=20, choices=FORMAS_PAGAMENTO)
    status = models.CharField(max_length=30, choices=STATUS_PEDIDO, default='AGUARDANDO_PAGAMENTO')
    data_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido {self.id} - {self.cliente.nome_completo}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    variacao_produto = models.ForeignKey(VariacaoProduto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario

    def __str__(self):
        return f"{self.quantidade}x {self.variacao_produto}"

class Parcela(models.Model):
    STATUS_PARCELA = [
        ('PENDENTE', 'Pendente'),
        ('PAGA', 'Paga'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='parcelas')
    numero_parcela = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_PARCELA, default='PENDENTE')

    @property
    def esta_atrasada(self):
        return self.status == 'PENDENTE' and self.data_vencimento < timezone.now().date()

    def __str__(self):
        return f"Parcela {self.numero_parcela} de {self.pedido.id} - R$ {self.valor}"
