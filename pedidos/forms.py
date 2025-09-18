from django import forms
from .models import Tarefa
from voluntarios.models import Voluntario 

class FormularioTarefa(forms.ModelForm):
    
    class Meta:
        model = Tarefa
        fields = [
            'titulo', 'descricao', 'status', 'prioridade', 
            'data_prevista_conclusao', 'voluntarios_responsaveis',
            'observacoes'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'data_prevista_conclusao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        labels = {
            'titulo': 'Título da Tarefa',
            'descricao': 'Descrição Detalhada',
            'data_prevista_conclusao': 'Prazo de Entrega (Opcional)',
            'voluntarios_responsaveis': 'Atribuir aos Voluntários (Opcional)',
        }
        help_texts = {
            'voluntarios_responsaveis': 'Selecione um ou mais voluntários ativos para esta tarefa.',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extrai o usuário dos kwargs
        super().__init__(*args, **kwargs)
        
        # Adicionar classes do Bootstrap e ajustar campos
        for field_name, field in self.fields.items():
            if field_name == 'voluntarios_responsaveis': 
                continue

            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            if not field.required: 
                field.widget.attrs.pop('required', None)
        
        if 'voluntarios_responsaveis' in self.fields: 
            self.fields['voluntarios_responsaveis'].queryset = Voluntario.objects.filter(ativo=True).order_by('nome_completo')
            self.fields['voluntarios_responsaveis'].widget = forms.CheckboxSelectMultiple()
        
        if 'status' in self.fields:
            self.fields['status'].widget.attrs.update({'class': 'form-select'})
        
        if 'prioridade' in self.fields:
            self.fields['prioridade'].widget.attrs.update({'class': 'form-select'})

        # Aplicar restrições para voluntários apenas na edição de uma tarefa existente
        if user and user.is_authenticated and hasattr(user, 'tipo_usuario') and user.tipo_usuario == 'VOLUNT' and self.instance and self.instance.pk:
            for field_name, field in self.fields.items():
                if field_name != 'status':
                    field.disabled = True 
            
            if 'status' in self.fields: # Garantir que status seja editável
                 self.fields['status'].disabled = False
