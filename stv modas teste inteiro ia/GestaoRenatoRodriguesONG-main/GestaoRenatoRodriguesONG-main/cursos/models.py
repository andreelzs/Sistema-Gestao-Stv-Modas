from django.db import models
from beneficiarios.models import Beneficiario

class Curso(models.Model):
    nome_curso = models.CharField(max_length=200, verbose_name="Nome do Curso")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return self.nome_curso

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"

class Certificado(models.Model):
    beneficiario = models.ForeignKey(Beneficiario, on_delete=models.CASCADE, related_name='certificados', verbose_name="Beneficiário")
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, related_name='certificados', verbose_name="Curso") # PROTECT para não deletar curso se houver certificados
    data_conclusao = models.DateField(verbose_name="Data de Conclusão")
    data_emissao_certificado = models.DateField(blank=True, null=True, verbose_name="Data de Emissão do Certificado")
    certificado_recebido = models.BooleanField(default=False, verbose_name="Certificado Físico Recebido")

    def __str__(self):
        return f"Certificado de {self.curso.nome_curso} para {self.beneficiario.nome_completo}"

    class Meta:
        verbose_name = "Certificado"
        verbose_name_plural = "Certificados"
        ordering = ['-data_conclusao', 'beneficiario__nome_completo']
        unique_together = ('beneficiario', 'curso', 'data_conclusao') # Evitar duplicidade exata
