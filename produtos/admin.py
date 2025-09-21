# Dentro do ficheiro: produtos/admin.py

from django.contrib import admin
from .models import Categoria, Cor, Tamanho, ProdutoBase, ImagemProduto, VariacaoProduto

@admin.register(Cor)
class CorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Tamanho)
class TamanhoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1

class VariacaoProdutoInline(admin.TabularInline):
    model = VariacaoProduto
    extra = 1
    fields = ('cor', 'tamanho', 'estoque', 'preco_venda')

@admin.register(ProdutoBase)
class ProdutoBaseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_venda_padrao', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome',)
    inlines = [ImagemProdutoInline, VariacaoProdutoInline]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(VariacaoProduto)
class VariacaoProdutoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'estoque', 'get_preco_venda')
    list_filter = ('produto_base', 'cor', 'tamanho')
    search_fields = ('produto_base__nome', 'cor__nome', 'tamanho__nome')