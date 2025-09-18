from django.db import models

class Beneficiario(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('NI', 'Não Informado'),
    ]

    ESCOLARIDADE_CHOICES = [
        ('FI', 'Fundamental Incompleto'),
        ('FC', 'Fundamental Completo'),
        ('MI', 'Médio Incompleto'),
        ('MC', 'Médio Completo'),
        ('NI', 'Não Informado'),
    ]

    nome_completo = models.CharField(max_length=255, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES, default='NI', verbose_name='Gênero')
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name='CPF', help_text='Formato: XXX.XXX.XXX-XX (Opcional)')
    rg = models.CharField(max_length=20, blank=True, null=True, verbose_name='RG', help_text='(Opcional)')
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name='CEP', help_text='Formato: XXXXX-XXX')
    logradouro = models.CharField(max_length=255, blank=True, null=True, verbose_name='Logradouro')
    numero_endereco = models.CharField(max_length=10, blank=True, null=True, verbose_name='Número')
    complemento_endereco = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name='UF') # Sigla do estado, ex: SP

    # Contato
    telefone_principal = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone Principal', help_text='Formato: (XX) XXXXX-XXXX')
    telefone_secundario = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone Secundário', help_text='(Opcional)')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='E-mail')

    # Informações Socioeconômicas e Educacionais
    escolaridade = models.CharField(max_length=2, choices=ESCOLARIDADE_CHOICES, default='NI', verbose_name='Escolaridade')
    ocupacao = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ocupação/Profissão')
    renda_familiar_aproximada = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, 
        verbose_name='Renda Familiar Mensal Aproximada (R$)',
        help_text='Valor em Reais. Ex: 1500.50'
    )
    
    # Outras informações
    como_conheceu_ong = models.TextField(blank=True, null=True, verbose_name='Como conheceu a ONG?')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações Adicionais')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_inativacao = models.DateTimeField(null=True, blank=True, verbose_name='Data de Inativação')

    # Campo para calcular idade (não armazenado, mas pode ser um property no modelo)
    @property
    def idade(self):
        from datetime import date
        today = date.today()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

    class Meta:
        verbose_name = 'Beneficiário'
        verbose_name_plural = 'Beneficiários'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

    def get_cpf_formatado(self):
        if self.cpf:
            cpf_numeros = ''.join(filter(str.isdigit, self.cpf))
            if len(cpf_numeros) == 11:
                return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
        return self.cpf or ""

    def get_rg_formatado(self):
        if self.rg:
            # Remove não dígitos, exceto X no final
            rg_val = ''.join(filter(str.isdigit, self.rg[:-1])) + \
                     (self.rg[-1] if self.rg[-1].upper() == 'X' else ''.join(filter(str.isdigit, self.rg[-1])))
            rg_val = rg_val.upper()
            
            # Formato RJ: XX.XXX.XXX-Y (9 caracteres)
            if len(rg_val) == 9:
                return f"{rg_val[0:2]}.{rg_val[2:5]}.{rg_val[5:8]}-{rg_val[8]}"
            # Outros formatos comuns (ex: 8 dígitos)
            elif len(rg_val) == 8: # XX.XXX.XXX
                 return f"{rg_val[0:2]}.{rg_val[2:5]}.{rg_val[5:8]}"
            # Adicionar mais lógicas se necessário ou apenas retornar o RG puro
        return self.rg or ""

    def _formatar_telefone(self, telefone_str):
        if telefone_str:
            tel_numeros = ''.join(filter(str.isdigit, telefone_str))
            if len(tel_numeros) == 11: # (XX) XXXXX-XXXX
                return f"({tel_numeros[:2]}) {tel_numeros[2:7]}-{tel_numeros[7:]}"
            elif len(tel_numeros) == 10: # (XX) XXXX-XXXX
                return f"({tel_numeros[:2]}) {tel_numeros[2:6]}-{tel_numeros[6:]}"
        return telefone_str or ""

    def get_telefone_principal_formatado(self):
        return self._formatar_telefone(self.telefone_principal)

    def get_telefone_secundario_formatado(self):
        return self._formatar_telefone(self.telefone_secundario)

    def get_cep_formatado(self):
        if self.cep:
            cep_numeros = ''.join(filter(str.isdigit, self.cep))
            if len(cep_numeros) == 8:
                return f"{cep_numeros[:5]}-{cep_numeros[5:]}"
        return self.cep or ""
