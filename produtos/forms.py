from django import forms
from django.forms import inlineformset_factory
from .models import ProdutoBase, VariacaoProduto, ImagemProduto, Categoria, Cor, Tamanho

class ProdutoBaseForm(forms.ModelForm):
    class Meta:
        model = ProdutoBase
        # Listamos os campos que devem aparecer no formulário
        fields = [
            'referencia',
            'nome',
            'descricao',
            'categoria',
            'marca',
            'preco_custo',
            'preco_venda_padrao',
            'ativo',
        ]
        # Podemos adicionar widgets para personalizar os campos, se necessário
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

class VariacaoProdutoForm(forms.ModelForm):
    class Meta:
        model = VariacaoProduto
        fields = ['cor', 'tamanho', 'estoque', 'preco_venda']

class ImagemProdutoForm(forms.ModelForm):
    class Meta:
        model = ImagemProduto
        fields = ['imagem']

# Formsets para variações e imagens
VariacaoProdutoFormSet = inlineformset_factory(
    ProdutoBase, 
    VariacaoProduto, 
    form=VariacaoProdutoForm,
    extra=1,
    can_delete=True
)

ImagemProdutoFormSet = inlineformset_factory(
    ProdutoBase, 
    ImagemProduto, 
    form=ImagemProdutoForm,
    extra=1,
    can_delete=True
)
