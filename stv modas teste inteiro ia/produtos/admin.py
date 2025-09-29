from django.contrib import admin
from .models import ProdutoBase, Categoria, Cor, Tamanho, ImagemProduto, VariacaoProduto, Marca

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Cor)
class CorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Tamanho)
class TamanhoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

class VariacaoProdutoInline(admin.TabularInline):
    model = VariacaoProduto
    extra = 1
    # Para permitir adicionar cor/tamanho diretamente do inline
    autocomplete_fields = ['cor', 'tamanho']

@admin.register(ProdutoBase)
class ProdutoBaseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'referencia', 'categoria', 'marca', 'preco_venda_padrao', 'ativo')
    list_filter = ('ativo', 'categoria', 'marca')
    search_fields = ('nome', 'referencia', 'descricao')
    inlines = [ImagemProdutoInline, VariacaoProdutoInline]


@admin.register(VariacaoProduto)
class VariacaoProdutoAdmin(admin.ModelAdmin):
    list_display = ('produto_base', 'cor', 'tamanho', 'estoque', 'get_preco_venda')
    search_fields = ('produto_base__nome', 'produto_base__referencia', 'cor__nome', 'tamanho__nome')
    list_filter = ('produto_base', 'cor', 'tamanho')
    autocomplete_fields = ['produto_base', 'cor', 'tamanho']
