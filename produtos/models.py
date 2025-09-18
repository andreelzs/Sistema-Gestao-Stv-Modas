# Dentro do arquivo: produtos/models.py

from django.db import models

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
    imagem_principal = models.ImageField(upload_to='produtos/', blank=True, null=True)
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Produto Base"
        verbose_name_plural = "Produtos Base"

    def __str__(self):
        return self.nome

class VariacaoProduto(models.Model):
    produto_base = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE, related_name='variacoes')
    cor = models.CharField(max_length=50, blank=True, null=True)
    tamanho = models.CharField(max_length=20, blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Se deixado em branco, usará o preço do produto base.")

    class Meta:
        verbose_name = "Variação de Produto"
        verbose_name_plural = "Variações de Produtos"
        unique_together = ('produto_base', 'cor', 'tamanho') # Garante que não haja variações duplicadas

    def __str__(self):
        return f"{self.produto_base.nome} ({self.cor or ''} - {self.tamanho or ''})"

    @property
    def get_preco_venda(self):
        return self.preco_venda or self.produto_base.preco_venda_padrao