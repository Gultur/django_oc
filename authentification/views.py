from django.shortcuts import (render, redirect)
from django.contrib.auth import (authenticate, login, logout)
from .forms import ConnexionForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required


def connexion(request):

    error = False
    form = ConnexionForm(request.POST or None)

    if form.is_valid():
        pseudo = form.cleaned_data['username']
        password = form.cleaned_data['password']
        # on utilise la methode qui permet de verifier si l'user existe
        user = authenticate(username=pseudo, password=password)
        if user is not None:
            # on connecte l'utilisateur
            login(request, user)
        else:
            error = True

    return render(request, 'authentification/connexion.html', locals())


def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))

@login_required
def vue_privee(request):
    return render(request, 'authentification/prive.html', locals())
