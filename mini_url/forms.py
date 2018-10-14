from django import forms
from .models import MiniURL


# si on utilise la class meta il faut ecrire forms.ModelForm au lieu de forms.form
class MiniURLForm(forms.ModelForm):
    class Meta:
        model = MiniURL
        fields = ('url', 'pseudo')
