from django.contrib import admin
from django import forms
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Pedido, ItemPedido, Parcela
from produtos.models import ProdutoBase, Cor, Tamanho, VariacaoProduto, Categoria

# Removendo ItemPedidoForm, vamos usar o inline padrão com autocomplete
# class ItemPedidoForm(forms.ModelForm):
#     produto_base = forms.ModelChoiceField(...)
#     cor = forms.ModelChoiceField(...)
#     tamanho = forms.ModelChoiceField(...)
#     class Meta:
#         model = ItemPedido
#         fields = ('produto_base', 'cor', 'tamanho', 'quantidade', 'preco_unitario', 'variacao_produto',)
#         widgets = {
#             'variacao_produto': forms.HiddenInput(attrs={'class': 'itempedido-variacao-input'}),
#         }
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if 'variacao_produto' in self.fields:
#             self.fields['variacao_produto'].label = ''
#         if self.instance and self.instance.pk and self.instance.variacao_produto:
#             self.initial['produto_base'] = self.instance.variacao_produto.produto_base
#             self.initial['cor'] = self.instance.variacao_produto.cor
#             self.initial['tamanho'] = self.instance.variacao_produto.tamanho

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    # Usaremos o autocomplete padrão do Django para variacao_produto
    autocomplete_fields = ['variacao_produto']
    # Os campos serão variacao_produto, quantidade e preco_unitario
    fields = ('variacao_produto', 'quantidade', 'preco_unitario',)

class ParcelaInline(admin.TabularInline):
    model = Parcela
    extra = 0

class PedidoAdminForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        # Validação da soma das parcelas
        # Esta validação será feita no backend após o formset ser salvo.
        # Precisamos de um mecanismo para aceder aos dados do formset de parcelas aqui.
        # Para simplificar, esta validação pode ser movida para save_model ou save_formset,
        # onde o formset de parcelas já está disponível.
        return cleaned_data

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    form = PedidoAdminForm
    list_display = ('id', 'cliente', 'valor_total', 'status', 'data_pedido')
    list_filter = ('status', 'forma_pagamento', 'data_pedido')
    search_fields = ('id', 'cliente__nome_completo')
    inlines = [ItemPedidoInline, ParcelaInline]
    autocomplete_fields = ['cliente']
    
    fieldsets = (
        (None, {
            'fields': ('cliente', 'valor_total', 'forma_pagamento', 'status',)
        }),
    )

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.min.js',
            'admin/js/jquery.init.js',
            'admin/js/autocomplete.js',
            'pedidos/js/pedido_form.js', # Nosso JS customizado
        )
        css = {
            'all': ('admin/css/autocomplete.css',)
        }
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_formset(self, request, form, formset, change):
        # Lógica de controle de estoque
        if formset.model == ItemPedido:
            instances = formset.save(commit=False)
            for instance in instances:
                # Se o item está sendo adicionado
                if not instance.pk:
                    instance.variacao_produto.estoque -= instance.quantidade
                else:
                    # Se o item está sendo modificado
                    original = ItemPedido.objects.get(pk=instance.pk)
                    diferenca = instance.quantidade - original.quantidade
                    instance.variacao_produto.estoque -= diferenca
                instance.variacao_produto.save()
            
            # Lida com itens deletados
            for obj in formset.deleted_objects:
                obj.variacao_produto.estoque += obj.quantidade
                obj.variacao_produto.save()

        formset.save()
        
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Validação da soma das parcelas no save_model, após o Pedido e suas Parcelas serem salvos
        if not obj.pk:
            return
        pass
