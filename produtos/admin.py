# Dentro do ficheiro: produtos/admin.py

from django.contrib import admin
from .models import Categoria, Cor, Tamanho, ProdutoBase, ImagemProduto, VariacaoProduto

# --- Novos admins para os modelos de atributos ---

@admin.register(Cor)
class CorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Tamanho)
class TamanhoAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

# --- Classes "Inline" para facilitar o cadastro ---

class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 1  # Mostra 1 campo para upload de imagem por defeito

class VariacaoProdutoInline(admin.TabularInline):
    model = VariacaoProduto
    extra = 1  # Mostra 1 campo para nova variação por defeito

# --- Admin principal do Produto, agora melhorado ---

@admin.register(ProdutoBase)
class ProdutoBaseAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco_venda_padrao', 'ativo')
    list_filter = ('categoria', 'ativo')
    search_fields = ('nome',)
    inlines = [ImagemProdutoInline, VariacaoProdutoInline] # Adiciona os inlines aqui

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)