# Dentro do arquivo: pedidos/models.py

from datetime import date
from django.db import models
from clientes.models import Cliente
from produtos.models import VariacaoProduto

class Pedido(models.Model):
    
    FORMAS_PAGAMENTO_CHOICES = [
        ('PIX', 'PIX'),
        ('CARTAO_CREDITO', 'Cartão de Crédito'),
        ('CARTAO_DEBITO', 'Cartão de Débito'),
        ('DINHEIRO', 'Dinheiro'),
        ('CREDIARIO', 'Crediário'),
    ]

    STATUS_PEDIDO_CHOICES = [
        ('AGUARDANDO_PAGAMENTO', 'Aguardando Pagamento'),
        ('EM_SEPARACAO', 'Em Separação'),
        ('PRONTO_PARA_ENTREGA', 'Pronto para Entrega'),
        ('ENTREGUE', 'Entregue'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    data_pedido = models.DateTimeField(auto_now_add=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    forma_pagamento = models.CharField(max_length=50, choices=FORMAS_PAGAMENTO_CHOICES)
    status = models.CharField(max_length=50, choices=STATUS_PEDIDO_CHOICES, default='AGUARDANDO_PAGAMENTO')

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido']

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente.nome_completo}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    variacao_produto = models.ForeignKey(VariacaoProduto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"

    def __str__(self):
        return f"{self.quantidade}x {self.variacao_produto.produto_base.nome}"

class Parcela(models.Model):

    STATUS_PARCELA_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('PAGA', 'Paga'),
    ]

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='parcelas')
    numero_parcela = models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_PARCELA_CHOICES, default='PENDENTE')

    class Meta:
        verbose_name = "Parcela"
        verbose_name_plural = "Parcelas"
        unique_together = ('pedido', 'numero_parcela')

    def __str__(self):
        return f"Parcela {self.numero_parcela} do Pedido #{self.pedido.id}"

    @property
    def esta_atrasada(self):
        """
        Retorna True se a parcela estiver com status 'PENDENTE' 
        e a data de vencimento já passou.
        """
        if self.status == 'PENDENTE' and self.data_vencimento < date.today():
            return True
        return False