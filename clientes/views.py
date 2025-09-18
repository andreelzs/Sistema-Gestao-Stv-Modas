from django.shortcuts import render
# No futuro, importaremos os models Cliente e Etiqueta aqui
# from .models import Cliente, Etiqueta

# As funções para listar, criar, editar e deletar clientes virão aqui.
# Por enquanto, pode ficar vazio ou com uma função de placeholder.

def listar_clientes(request):
    return render(request, 'clientes/listar_clientes.html') # Apenas um exemplo