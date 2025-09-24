from django import forms
from .models import Beneficiario

class FormularioBeneficiario(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = [
            'nome_completo', 'data_nascimento', 'genero', 'cpf', 'rg',
            'cep', 'logradouro', 'numero_endereco', 'complemento_endereco', 
            'bairro', 'cidade', 'estado',
            'telefone_principal', 'telefone_secundario', 'email',
            'escolaridade', 'ocupacao', 'renda_familiar_aproximada',
            'como_conheceu_ong', 'observacoes', 'ativo'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'endereco': forms.Textarea(attrs={'rows': 3}),
            'como_conheceu_ong': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'nome_completo': 'Nome Completo do Beneficiário',
            'numero_endereco': 'Número',
            'complemento_endereco': 'Complemento',
            'estado': 'UF (Ex: SP)',
            'renda_familiar_aproximada': 'Renda Familiar Mensal Aproximada (R$)',
        }
        help_texts = {
            'cpf': 'Formato: XXX.XXX.XXX-XX (Opcional, mas recomendado)',
            'cep': 'Formato: XXXXX-XXX (Opcional)',
            'telefone_principal': 'Formato: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX',
            'renda_familiar_aproximada': 'Use ponto para decimais. Ex: 1500.50',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Adiciona a classe 'form-control' do Bootstrap, exceto para checkboxes
            if not isinstance(field.widget, forms.CheckboxInput):
                current_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{current_class} form-control'.strip()
            elif isinstance(field.widget, forms.CheckboxInput): # Para checkboxes Bootstrap 5
                current_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{current_class} form-check-input'.strip()

            # Campos opcionais podem não ter o atributo 'required' no widget
            # mas o campo do formulário em si terá.
            # Se o campo não for obrigatório no modelo, não adicionamos 'required' no HTML
            if not field.required:
                field.widget.attrs.pop('required', None)
        
        # Adicionar placeholders
        field_configs = {
            'rg': {'placeholder': 'Ex: 12.345.678-9', 'maxlength': '12'},
            'cpf': {'placeholder': 'Ex: 123.456.789-00', 'maxlength': '14'},
            'telefone_principal': {'placeholder': 'Ex: (21) 99999-9999', 'maxlength': '15'},
            'telefone_secundario': {'placeholder': 'Ex: (21) 99999-9999', 'maxlength': '15'},
            'cep': {'placeholder': 'Ex: 12345-678', 'maxlength': '9'},
        }
        for field_name, config in field_configs.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(config)

    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep: 
            cep_numeros = ''.join(filter(str.isdigit, cep))
            if len(cep_numeros) != 8:
                raise forms.ValidationError("CEP inválido. Deve conter exatamente 8 dígitos numéricos.")
            return cep_numeros 
        return cep 
