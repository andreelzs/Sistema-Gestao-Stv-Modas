from django import forms
from .models import Certificado, Curso
from beneficiarios.models import Beneficiario

class CertificadoForm(forms.ModelForm):
    
    curso = forms.ModelChoiceField(
        queryset=Curso.objects.all().order_by('nome_curso'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Curso"
    )

    class Meta:
        model = Certificado
        fields = ['curso', 'data_conclusao', 'data_emissao_certificado', 'certificado_recebido']
        widgets = {
            'data_conclusao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'data_emissao_certificado': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'certificado_recebido': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'curso': "Curso", # HTML removido
            'data_conclusao': "Data de Conclusão", # HTML removido
            'data_emissao_certificado': "Data de Emissão do Certificado (Opcional)", # Será tratado por JS
            'certificado_recebido': "Certificado Físico Recebido pelo Beneficiário",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_emissao_certificado'].required = False # Tornar opcional explicitamente

    def clean(self):
        cleaned_data = super().clean()
        certificado_recebido = cleaned_data.get('certificado_recebido')
        data_emissao_certificado = cleaned_data.get('data_emissao_certificado')

        if certificado_recebido and not data_emissao_certificado:
            # A mensagem de erro será associada ao campo 'data_emissao_certificado'
            self.add_error('data_emissao_certificado', 
                           forms.ValidationError("A data de emissão do certificado é obrigatória se o certificado foi marcado como recebido."))
        
        # Se 'certificado_recebido' for True, então 'data_emissao_certificado' deve ser obrigatório.
        # Podemos também ajustar o atributo 'required' do campo dinamicamente aqui,
        # mas a validação com add_error já impede o formulário de ser válido.
        # Para o JavaScript no frontend, ele manipulará o visual (asterisco).
        
        return cleaned_data


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome_curso', 'descricao']
        widgets = {
            'nome_curso': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'nome_curso': "Nome do Curso",
            'descricao': "Descrição (Opcional)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].required = False

    def clean_nome_curso(self):
        nome_curso_digitado = self.cleaned_data.get('nome_curso')
        if nome_curso_digitado:
            query = Curso.objects.filter(nome_curso__iexact=nome_curso_digitado)
            
            # Se estiver editando um curso existente (self.instance.pk existe),
            # precisamos excluí-lo da verificação para permitir salvar sem alterar o nome.
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise forms.ValidationError(
                    "Este nome de curso ja foi cadastrado. Por favor, escolha outro."
                )
        return nome_curso_digitado
