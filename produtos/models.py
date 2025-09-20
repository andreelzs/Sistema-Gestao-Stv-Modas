# Dentro do ficheiro: produtos/models.py

from django.db import models

# --- NOVOS MODELOS PARA CORES E TAMANHOS ---
class Cor(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Tamanho(models.Model):
    nome = models.CharField(max_length=20, unique=True, help_text='Ex: P, M, G, 40, 42')

    def __str__(self):
        return self.nome

# --- MODELOS ANTERIORES, AGORA ATUALIZADOS ---

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome

class ProdutoBase(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda_padrao = models.DecimalField(max_digits=10, decimal_places=2)
    # O campo de imagem principal foi removido daqui
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Produto Base"
        verbose_name_plural = "Produtos Base"

    def __str__(self):
        return self.nome

# --- NOVO MODELO PARA GERIR MÚLTIPLAS IMAGENS ---
class ImagemProduto(models.Model):
    produto = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='produtos/')

    class Meta:
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens do Produto"

# --- VARIAÇÃO DE PRODUTO ATUALIZADA ---
class VariacaoProduto(models.Model):
    produto_base = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE, related_name='variacoes')
    # Campos de texto livre foram substituídos por chaves estrangeiras
    cor = models.ForeignKey(Cor, on_delete=models.PROTECT, blank=True, null=True)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.PROTECT, blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Se deixado em branco, usará o preço do produto base.")

    class Meta:
        verbose_name = "Variação de Produto"
        verbose_name_plural = "Variações de Produtos"
        unique_together = ('produto_base', 'cor', 'tamanho')

    def __str__(self):
        cor_nome = self.cor.nome if self.cor else ''
        tamanho_nome = self.tamanho.nome if self.tamanho else ''
        return f"{self.produto_base.nome} ({cor_nome} - {tamanho_nome})"

    @property
    def get_preco_venda(self):
        return self.preco_venda or self.produto_base.preco_venda_padrao