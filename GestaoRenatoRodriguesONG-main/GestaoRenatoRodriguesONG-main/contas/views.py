from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

class LoginUsuarioView(auth_views.LoginView):
    template_name = 'contas/login.html'
    # Se o login for bem-sucedido, redireciona para a página inicial do core.
    success_url = reverse_lazy('core:pagina_inicial') 

    def form_valid(self, form):
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Se o usuário já está logado, redireciona para a success_url
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class LogoutUsuarioView(auth_views.LogoutView):
    # Após o logout, redireciona para a página inicial do core.
    next_page = reverse_lazy('core:pagina_inicial')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

