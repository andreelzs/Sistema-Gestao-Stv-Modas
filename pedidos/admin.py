# Dentro do ficheiro: pedidos/admin.py

from django import forms
from django.contrib import admin
from .models import Pedido, ItemPedido, Parcela
from produtos.models import ProdutoBase
from dateutil.relativedelta import relativedelta

# --- Formulário Personalizado para o Item do Pedido (CORRIGIDO) ---

class ItemPedidoForm(forms.ModelForm):
    produto_base = forms.ModelChoiceField(
        queryset=ProdutoBase.objects.filter(ativo=True).order_by('nome'),
        label='Produto',
        required=False,
        widget=forms.Select(attrs={'class': 'item-produto-base'})
    )
    # Estes campos serão preenchidos dinamicamente pelo JavaScript.
    cor = forms.ChoiceField(label='Cor', required=False, choices=[('', '---')], widget=forms.Select(attrs={'class': 'item-cor'}))
    tamanho = forms.ChoiceField(label='Tamanho', required=False, choices=[('', '---')], widget=forms.Select(attrs={'class': 'item-tamanho'}))

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

# --- Admin para Parcelas ---

class ParcelaInline(admin.TabularInline):
    model = Parcela
    extra = 0
    # Adicionamos 'esta_atrasada' para visualização, se desejado
    readonly_fields = ('numero_parcela', 'valor', 'data_vencimento', 'status', 'esta_atrasada')

# --- Formulário para Pedidos ---

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

# --- Admin Principal para Pedidos ---

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
        # --- LÓGICA DE STOCK AVANÇADA COM COMENTÁRIOS ---
        
        # ETAPA 1: Lidar com itens removidos do pedido.
        # O Django coloca os formulários marcados para exclusão em `formset.deleted_forms`.
        # Percorremos cada um deles para devolver o seu stock.
        for form_item in formset.deleted_forms:
            if form_item.instance.pk: # Confirma que o item realmente existia e não era apenas uma linha em branco.
                item_original = form_item.instance
                # Devolve a quantidade do item removido de volta para o stock da variação do produto.
                item_original.variacao_produto.estoque += item_original.quantidade
                item_original.variacao_produto.save()

        # ETAPA 2: Lidar com itens que foram alterados (não removidos nem novos).
        # `formset.initial_forms` contém os formulários de itens que já existiam no pedido.
        instances = formset.save(commit=False)
        for instance in instances:
             if instance.pk: # Se o item já existe (edição)
                quantidade_antiga = ItemPedido.objects.get(pk=instance.pk).quantidade
                quantidade_nova = instance.quantidade
                diferenca = quantidade_nova - quantidade_antiga

                # Validação de stock: só verificamos se a diferença for positiva (tentativa de retirar mais).
                if instance.variacao_produto.estoque < diferenca:
                    # Se não houver stock suficiente para cobrir a diferença, ignoramos esta alteração.
                    continue
                
                # Se houver stock, ajustamos o stock com a diferença calculada.
                instance.variacao_produto.estoque -= diferenca
                instance.variacao_produto.save()
        
        # ETAPA 3: Lidar com itens completamente novos que foram adicionados.
        # `formset.new_forms` não é fiável aqui, por isso iteramos sobre as instâncias sem pk
        for instance in instances:
            if not instance.pk: # Se é um item novo
                # Validação de stock simples: a quantidade nova não pode ser maior que o stock total.
                if instance.variacao_produto.estoque < instance.quantidade:
                    continue # Ignora este novo item se não houver stock.
                
                # Dá baixa da quantidade total do novo item no stock.
                instance.variacao_produto.estoque -= instance.quantidade
                instance.variacao_produto.save()

        # Depois de toda a lógica de stock, salvamos as alterações no formset.
        formset.save()
        super().save_formset(request, form, formset, change)

        # Revalidação final do valor total do pedido para garantir consistência.
        pedido = form.instance
        valor_calculado = sum(item.quantidade * item.preco_unitario for item in pedido.itens.all())
        if pedido.valor_total != valor_calculado:
             pedido.valor_total = valor_calculado
             pedido.save()