from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home') # Redireciona para a home após o registo
    else:
        form = UserCreationForm()
    return render(request, 'contas/register.html', {'form': form})
