from django.shortcuts import render

def pagina_inicial(request):
    # Futuramente, podemos adicionar lógicas aqui, como mostrar o dashboard.
    contexto = {
        'titulo': 'Bem-vindo ao Sistema STV Modas'
    }
    return render(request, 'core/pagina_inicial.html', contexto)