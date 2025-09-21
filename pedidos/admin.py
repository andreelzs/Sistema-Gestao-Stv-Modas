from django import forms
from django.contrib import admin
from .models import Pedido, ItemPedido, Parcela
from produtos.models import ProdutoBase, VariacaoProduto
from dateutil.relativedelta import relativedelta

# --- Formulário Personalizado para o Item do Pedido ---
class ItemPedidoForm(forms.ModelForm):
    produto_base = forms.ModelChoiceField(
        queryset=ProdutoBase.objects.filter(ativo=True),
        label='Produto',
        widget=forms.Select(attrs={'class': 'item-produto-base'})
    )
    cor = forms.ChoiceField(label='Cor', required=False, widget=forms.Select(attrs={'class': 'item-cor'}))
    tamanho = forms.ChoiceField(label='Tamanho', required=False, widget=forms.Select(attrs={'class': 'item-tamanho'}))

    class Meta:
        model = ItemPedido
        fields = ('produto_base', 'cor', 'tamanho', 'quantidade', 'preco_unitario', 'variacao_produto')
        widgets = {
            'variacao_produto': forms.HiddenInput(),
        }


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    form = ItemPedidoForm
    extra = 1

# --- O resto do admin ---
class ParcelaInline(admin.TabularInline):
    model = Parcela
    extra = 0
    readonly_fields = ('numero_parcela', 'valor', 'data_vencimento', 'status')

class PedidoAdminForm(forms.ModelForm):
    numero_de_parcelas = forms.IntegerField(
        label='Número de Parcelas',
        min_value=1,
        initial=1,
        required=False,
        widget=forms.NumberInput(attrs={'style': 'width: 80px;'})
    )
    data_primeira_parcela = forms.DateField(
        label='Data da 1ª Parcela',
        required=False,
        widget=admin.widgets.AdminDateWidget
    )

    class Meta:
        model = Pedido
        fields = '__all__'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    form = PedidoAdminForm
    list_display = ('id', 'cliente', 'data_pedido', 'valor_total', 'status')
    list_filter = ('status', 'forma_pagamento')
    search_fields = ('cliente__nome_completo', 'id')
    inlines = [ItemPedidoInline, ParcelaInline]

    fieldsets = (
        (None, {
            'fields': ('cliente', 'forma_pagamento', 'status', 'valor_total')
        }),
        ('Gerador de Parcelas (para Crediário)', {
            'fields': ('numero_de_parcelas', 'data_primeira_parcela'),
            'description': 'Preencha e clique no botão "Gerar Parcelas" que aparecerá ao lado.'
        }),
    )

    class Media:
        js = ('pedidos/js/pedido_admin.js',)

    def save_formset(self, request, form, formset, change):
        # LÓGICA DE ESTOQUE AVANÇADA
        
        # Primeiro, lidamos com os itens que foram marcados para exclusão
        for form_item in formset.deleted_forms:
            if form_item.instance.pk: # Se o item realmente existia na base de dados
                item_original = form_item.instance
                # Devolve a quantidade ao stock
                item_original.variacao_produto.estoque += item_original.quantidade
                item_original.variacao_produto.save()

        # Depois, lidamos com os itens que foram adicionados ou alterados
        for form_item in formset.initial_forms:
            if form_item.has_changed():
                item_alterado = form_item.instance
                quantidade_antiga = form_item.initial.get('quantidade', 0)
                quantidade_nova = form_item.cleaned_data.get('quantidade', 0)
                diferenca = quantidade_nova - quantidade_antiga
                
                # Validação de estoque
                if item_alterado.variacao_produto.estoque < diferenca:
                    # Idealmente, aqui mostrariamos uma mensagem de erro ao utilizador
                    # Por agora, simplesmente não permitimos a alteração
                    continue 
                
                # Ajusta o estoque com a diferença
                item_alterado.variacao_produto.estoque -= diferenca
                item_alterado.variacao_produto.save()
        
        # Finalmente, lidamos com os itens novos
        for form_item in formset.new_forms:
            if form_item.is_valid() and form_item.cleaned_data.get('variacao_produto'):
                item_novo = form_item.instance
                quantidade_nova = form_item.cleaned_data.get('quantidade', 0)
                
                # Validação de stock
                if item_novo.variacao_produto.estoque < quantidade_nova:
                    continue # Não permite a venda
                
                # Dá baixa do stock
                item_novo.variacao_produto.estoque -= quantidade_nova
                item_novo.variacao_produto.save()

        # Salva todas as alterações no formset (itens e parcelas)
        super().save_formset(request, form, formset, change)

        # Revalidação do valor total do pedido
        pedido = form.instance
        valor_calculado = sum(item.quantidade * item.preco_unitario for item in pedido.itens.all())
        if pedido.valor_total != valor_calculado:
             pedido.valor_total = valor_calculado
             pedido.save()