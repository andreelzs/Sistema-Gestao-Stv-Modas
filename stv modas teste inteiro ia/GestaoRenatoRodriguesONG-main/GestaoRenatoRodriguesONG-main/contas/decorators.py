from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
# from django.http import HttpResponseForbidden # Alternativa para resposta, se preferir erro 403 direto

def admin_required(view_func):
    @wraps(view_func) # Preserva metadados da função original (nome, docstring, etc.)
    def _wrapped_view(request, *args, **kwargs):
        # Primeiro, verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            # Se @login_required não for usado antes do @admin_required, 
            # este redirecionamento para login é uma boa salvaguarda.
            # Idealmente, use @login_required primeiro na pilha de decorators.
            return redirect('contas:login') # Redireciona para a página de login

        # Verifica se o usuário tem o atributo 'tipo_usuario' e se é 'ADMIN'
        if hasattr(request.user, 'tipo_usuario') and request.user.tipo_usuario == 'ADMIN':
            return view_func(request, *args, **kwargs) # Permite acesso à view original
        else:
            # Se não for admin, exibe mensagem de erro e redireciona
            messages.error(request, 'Você não tem permissão para acessar esta página ou realizar esta ação.')
            # Redireciona para uma página segura, como a página inicial do core ou o dashboard
            # return HttpResponseForbidden('Acesso negado.') # Alternativa
            return redirect('core:pagina_inicial') 
    return _wrapped_view

# Você pode adicionar outros decorators aqui no futuro, se necessário
# Ex: def colaborador_required(view_func): ...
