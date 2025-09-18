from django.contrib import admin
from .models import Pedido, ItemPedido, Parcela

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ('variacao_produto', 'quantidade', 'preco_unitario') # Apenas visualização

class ParcelaInline(admin.TabularInline):
    model = Parcela
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'data_pedido', 'valor_total', 'status')
    list_filter = ('status', 'forma_pagamento')
    search_fields = ('cliente__nome_completo', 'id')
    inlines = [ItemPedidoInline, ParcelaInline]