from django.db import models
from django.conf import settings

class Voluntario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        help_text='Conta de usuário associada a este voluntário.'
    )
    nome_completo = models.CharField(max_length=255, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF', help_text='Formato: XXX.XXX.XXX-XX')
    rg = models.CharField(max_length=10, verbose_name='RG') # Tornando obrigatório
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone Celular', help_text='Formato: (XX) XXXXX-XXXX')
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name='CEP', help_text='Formato: XXXXX-XXX')
    logradouro = models.CharField(max_length=255, blank=True, null=True, verbose_name='Logradouro')
    numero_endereco = models.CharField(max_length=10, blank=True, null=True, verbose_name='Número')
    complemento_endereco = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name='UF') # Sigla do estado, ex: SP

    areas_interesse = models.TextField(blank=True, null=True, verbose_name='Áreas de Interesse', help_text='Descreva as áreas em que o voluntário tem interesse em atuar.')
    
    # Disponibilidade Semanal
    disp_seg_m = models.BooleanField(default=False, verbose_name='Segunda (Manhã)')
    disp_seg_t = models.BooleanField(default=False, verbose_name='Segunda (Tarde)')
    disp_seg_n = models.BooleanField(default=False, verbose_name='Segunda (Noite)')
    disp_ter_m = models.BooleanField(default=False, verbose_name='Terça (Manhã)')
    disp_ter_t = models.BooleanField(default=False, verbose_name='Terça (Tarde)')
    disp_ter_n = models.BooleanField(default=False, verbose_name='Terça (Noite)')
    disp_qua_m = models.BooleanField(default=False, verbose_name='Quarta (Manhã)')
    disp_qua_t = models.BooleanField(default=False, verbose_name='Quarta (Tarde)')
    disp_qua_n = models.BooleanField(default=False, verbose_name='Quarta (Noite)')
    disp_qui_m = models.BooleanField(default=False, verbose_name='Quinta (Manhã)')
    disp_qui_t = models.BooleanField(default=False, verbose_name='Quinta (Tarde)')
    disp_qui_n = models.BooleanField(default=False, verbose_name='Quinta (Noite)')
    disp_sex_m = models.BooleanField(default=False, verbose_name='Sexta (Manhã)')
    disp_sex_t = models.BooleanField(default=False, verbose_name='Sexta (Tarde)')
    disp_sex_n = models.BooleanField(default=False, verbose_name='Sexta (Noite)')
    disp_sab_m = models.BooleanField(default=False, verbose_name='Sábado (Manhã)')
    disp_sab_t = models.BooleanField(default=False, verbose_name='Sábado (Tarde)')
    disp_sab_n = models.BooleanField(default=False, verbose_name='Sábado (Noite)')
    disp_dom_m = models.BooleanField(default=False, verbose_name='Domingo (Manhã)')
    disp_dom_t = models.BooleanField(default=False, verbose_name='Domingo (Tarde)')
    disp_dom_n = models.BooleanField(default=False, verbose_name='Domingo (Noite)')

    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    data_inativacao = models.DateTimeField(null=True, blank=True, verbose_name='Data de Inativação')

    class Meta:
        verbose_name = 'Voluntário'
        verbose_name_plural = 'Voluntários'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

    def get_rg_formatado(self):
        if self.rg:
            # Formato RJ: XX.XXX.XXX-X (total 9 caracteres com DV)
            # Se o RG armazenado tiver 9 caracteres (8 números + DV)
            if len(self.rg) == 9:
                return f"{self.rg[0:2]}.{self.rg[2:5]}.{self.rg[5:8]}-{self.rg[8]}"
            
            elif len(self.rg) == 8:
                 return f"{self.rg[0:2]}.{self.rg[2:5]}.{self.rg[5:8]}"
    
            return self.rg 
        return ""

    def get_cpf_formatado(self):
        if self.cpf:
            cpf_numeros = ''.join(filter(str.isdigit, self.cpf))
            if len(cpf_numeros) == 11:
                return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
        return self.cpf or ""

    def get_telefone_formatado(self):
        if self.telefone:
            tel_numeros = ''.join(filter(str.isdigit, self.telefone))
            if len(tel_numeros) == 11: # (XX) XXXXX-XXXX
                return f"({tel_numeros[:2]}) {tel_numeros[2:7]}-{tel_numeros[7:]}"
            elif len(tel_numeros) == 10: # (XX) XXXX-XXXX
                return f"({tel_numeros[:2]}) {tel_numeros[2:6]}-{tel_numeros[6:]}"
        return self.telefone or ""

    def get_cep_formatado(self):
        if self.cep:
            cep_numeros = ''.join(filter(str.isdigit, self.cep))
            if len(cep_numeros) == 8:
                return f"{cep_numeros[:5]}-{cep_numeros[5:]}"
        return self.cep or ""

    def get_disponibilidade_formatada(self):
        dias_semana = [
            ("Segunda", self.disp_seg_m, self.disp_seg_t, self.disp_seg_n),
            ("Terça", self.disp_ter_m, self.disp_ter_t, self.disp_ter_n),
            ("Quarta", self.disp_qua_m, self.disp_qua_t, self.disp_qua_n),
            ("Quinta", self.disp_qui_m, self.disp_qui_t, self.disp_qui_n),
            ("Sexta", self.disp_sex_m, self.disp_sex_t, self.disp_sex_n),
            ("Sábado", self.disp_sab_m, self.disp_sab_t, self.disp_sab_n),
            ("Domingo", self.disp_dom_m, self.disp_dom_t, self.disp_dom_n),
        ]
        turnos_nomes = ["Manhã", "Tarde", "Noite"]
        disponibilidade_formatada = []
        
        for nome_dia, disp_m, disp_t, disp_n in dias_semana:
            turnos_do_dia = []
            if disp_m:
                turnos_do_dia.append(turnos_nomes[0])
            if disp_t:
                turnos_do_dia.append(turnos_nomes[1])
            if disp_n:
                turnos_do_dia.append(turnos_nomes[2])
            
            if turnos_do_dia:
                disponibilidade_formatada.append({
                    'dia': nome_dia,
                    'turnos': ", ".join(turnos_do_dia)
                })
        return disponibilidade_formatada
