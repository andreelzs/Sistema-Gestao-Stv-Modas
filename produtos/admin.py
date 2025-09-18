from django.contrib import admin
from .models import Categoria, ProdutoBase, VariacaoProduto

class VariacaoProdutoInline(admin.TabularInline):
    model = VariacaoProduto
    extra = 1  # Quantos formulários de variação em branco mostrar

@admin.register(ProdutoBase)
class ProdutoBaseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_venda_padrao', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome',)
    inlines = [VariacaoProdutoInline]

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)