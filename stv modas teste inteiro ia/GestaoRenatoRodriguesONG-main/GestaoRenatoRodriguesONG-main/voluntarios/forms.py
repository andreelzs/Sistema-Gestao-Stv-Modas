from django import forms
from .models import Voluntario
from contas.models import Usuario # Precisamos acessar o modelo Usuario para criar o formulário

class FormularioVoluntario(forms.ModelForm):
    # Campos do modelo Usuario que queremos no formulário de Voluntario
    # Estes não são campos diretos do modelo Voluntario, então os definimos aqui
    # e os trataremos na view.
    username = forms.CharField(label='Nome de Usuário (para login)', max_length=150)
    email = forms.EmailField(label='Email (para login e contato)', required=False)
    password = forms.CharField(label='Senha (para login)', widget=forms.PasswordInput, min_length=8)
    confirmar_password = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput, min_length=8)
    tipo_conta_usuario = forms.ChoiceField(
        label='Tipo de Conta do Usuário',
        choices=Usuario.TIPOS_USUARIO,
        widget=forms.RadioSelect,
        initial='COLAB' # Padrão para Colaborador
    )

    class Meta:
        model = Voluntario
        # Incluir campos do modelo Voluntario
        fields = [
            'nome_completo', 'cpf', 'rg', 'data_nascimento', 
            'telefone', 
            'cep', 'logradouro', 'numero_endereco', 'complemento_endereco', 'bairro', 'cidade', 'estado',
            'areas_interesse',

            'disp_seg_m', 'disp_seg_t', 'disp_seg_n',
            'disp_ter_m', 'disp_ter_t', 'disp_ter_n',
            'disp_qua_m', 'disp_qua_t', 'disp_qua_n',
            'disp_qui_m', 'disp_qui_t', 'disp_qui_n',
            'disp_sex_m', 'disp_sex_t', 'disp_sex_n',
            'disp_sab_m', 'disp_sab_t', 'disp_sab_n',
            'disp_dom_m', 'disp_dom_t', 'disp_dom_n',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'areas_interesse': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Extrair o usuário da requisição, se passado pela view
        self.request_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Se estiver editando um voluntário existente, podemos preencher os campos do usuário
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario'):
            self.fields['username'].initial = self.instance.usuario.username
            self.fields['email'].initial = self.instance.usuario.email
            self.fields['tipo_conta_usuario'].initial = self.instance.usuario.tipo_usuario
            # Não preenchemos a senha por segurança e usabilidade
            self.fields['password'].required = False
            self.fields['confirmar_password'].required = False
        
        # Adicionar classes do Bootstrap aos campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.RadioSelect):
                pass
            elif isinstance(field.widget, forms.CheckboxInput):
                # Para checkboxes individuais (não parte de um CheckboxSelectMultiple)
                current_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{current_class} form-check-input'.strip()
            elif not isinstance(field.widget, forms.CheckboxSelectMultiple):
                # Aplicar form-control a outros campos, exceto CheckboxSelectMultiple
                current_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{current_class} form-control'.strip()
        
        # Adicionar placeholder para RG
        if 'rg' in self.fields:
            self.fields['rg'].widget.attrs.update({
                'placeholder': 'Ex: 12.345.678-9',
                'maxlength': '12' 
            })
        if 'cpf' in self.fields:
            self.fields['cpf'].widget.attrs.update({
                'placeholder': 'Ex: 123.456.789-00',
                'maxlength': '14' 
            })
        if 'telefone' in self.fields:
            self.fields['telefone'].widget.attrs.update({
                'placeholder': 'Ex: (21) 99999-9999',
                'maxlength': '15' 
            })
        
        # Restringir edição do tipo de conta para voluntários editando o próprio perfil
        if self.request_user and self.request_user.is_authenticated and \
           hasattr(self.request_user, 'tipo_usuario') and self.request_user.tipo_usuario == 'VOLUNT' and \
           self.instance and hasattr(self.instance, 'usuario') and self.instance.usuario == self.request_user:
            if 'tipo_conta_usuario' in self.fields:
                self.fields['tipo_conta_usuario'].disabled = True

    def clean_rg(self):
        rg = self.cleaned_data.get('rg')
        if not rg:
            return rg

        rg_numeros = ""
        if len(rg) > 0:
            if rg[-1].upper() == 'X':
                rg_numeros = ''.join(filter(str.isdigit, rg[:-1])) + 'X'
            else:
                rg_numeros = ''.join(filter(str.isdigit, rg))
        
        if not (6 <= len(rg_numeros) <= 10):
            raise forms.ValidationError(
                "O RG deve conter de 6 a 10 caracteres (números e, opcionalmente, 'X' no final)."
            )

        # Verifica se todos os caracteres são dígitos, exceto o último que pode ser X
        if len(rg_numeros) > 0:
            # Se o último caractere for X, verifica se todos os anteriores são dígitos
            if rg_numeros[-1].upper() == 'X':
                if not rg_numeros[:-1].isdigit():
                    raise forms.ValidationError("RG inválido. Se o dígito verificador for 'X', os caracteres anteriores devem ser números.")
            # Se o último caractere não for X, verifica se todos são dígitos
            elif not rg_numeros.isdigit():
                raise forms.ValidationError("RG deve conter apenas números, ou terminar com 'X'.")
            
        elif not rg_numeros: 
             raise forms.ValidationError("Este campo é obrigatório.")


        return rg_numeros.upper()
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Se estiver editando e o username não mudou, permite.
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario.username == username:
            return username
        # Caso contrário, verifica se o username já existe.
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso. Por favor, escolha outro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Permite email vazio se não for obrigatório
        if not email and not self.fields['email'].required:
            return email
            
        # Se estiver editando e o email não mudou, permite.
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario.email == email:
            return email
        # Caso contrário, verifica se o email já existe.
        if email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado. Por favor, use outro ou deixe em branco se opcional.")
        return email

    def clean_confirmar_password(self):
        password = self.cleaned_data.get("password")
        confirmar_password = self.cleaned_data.get("confirmar_password")

        # Se estamos editando e a senha não foi fornecida, não há nada a validar aqui.
        if self.instance and self.instance.pk and not password:
            return confirmar_password

        if password and confirmar_password and password != confirmar_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return confirmar_password

    def save(self, commit=True):
        print(f"DEBUG: FormularioVoluntario.save() chamado. commit={commit}")
        print(f"DEBUG: cleaned_data: {self.cleaned_data}")

        is_new_voluntario = not (self.instance and self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario)
        
        print(f"DEBUG: is_new_voluntario: {is_new_voluntario}")

        if is_new_voluntario:
            print("DEBUG: Criando novo usuário...")
            try:
                user = Usuario.objects.create_user(
                    username=self.cleaned_data['username'],
                    email=self.cleaned_data.get('email'),
                    password=self.cleaned_data['password']
                )
                user.tipo_usuario = self.cleaned_data['tipo_conta_usuario'] # Definido pelo formulário
                print(f"DEBUG: Novo usuário criado (antes do save): id={user.id}, username={user.username}, tipo={user.tipo_usuario}, is_active={user.is_active}")
                if commit:
                    user.save()
                    print(f"DEBUG: Novo usuário salvo. Senha hasheada: {user.password}")
                self.instance.usuario = user
            except Exception as e:
                print(f"DEBUG: Erro ao criar usuário: {e}")
                raise # Re-levanta a exceção para não mascarar o erro
        else:
            print(f"DEBUG: Atualizando usuário existente: {self.instance.usuario.username}")
            user = self.instance.usuario
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data.get('email')
            user.tipo_usuario = self.cleaned_data['tipo_conta_usuario'] # Atualiza o tipo de usuário
            
            nova_senha = self.cleaned_data.get("password")
            if nova_senha:
                user.set_password(nova_senha)
                print(f"DEBUG: Senha do usuário atualizada.")
            
            if commit:
                user.save()
                print(f"DEBUG: Usuário existente salvo. Tipo: {user.tipo_usuario}, Senha hasheada: {user.password}")
        
        print("DEBUG: Salvando instância de Voluntario...")
        voluntario = super().save(commit=commit)
        print(f"DEBUG: Voluntario salvo: {voluntario}, Usuário associado: {voluntario.usuario}")
        return voluntario
