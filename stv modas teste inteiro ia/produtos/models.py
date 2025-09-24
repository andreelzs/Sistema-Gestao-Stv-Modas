from django.db import models

class Cor(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Tamanho(models.Model):
    nome = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

class ProdutoBase(models.Model):
    referencia = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda_padrao = models.DecimalField(max_digits=10, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} ({self.referencia})"

class ImagemProduto(models.Model):
    produto = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='produtos/')

    def __str__(self):
        return f"Imagem de {self.produto.nome}"

class VariacaoProduto(models.Model):
    produto_base = models.ForeignKey(ProdutoBase, on_delete=models.CASCADE, related_name='variacoes')
    cor = models.ForeignKey(Cor, on_delete=models.PROTECT, blank=True, null=True)
    tamanho = models.ForeignKey(Tamanho, on_delete=models.PROTECT, blank=True, null=True)
    estoque = models.PositiveIntegerField(default=0)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    @property
    def get_preco_venda(self):
        return self.preco_venda or self.produto_base.preco_venda_padrao

    def __str__(self):
        return f"{self.produto_base.nome} - {self.cor} / {self.tamanho}"
