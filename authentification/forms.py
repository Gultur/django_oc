from django import forms


class ConnexionForm(forms.Form):

    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    # forms.PasswordInput permet de cacher le mot de passe
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
