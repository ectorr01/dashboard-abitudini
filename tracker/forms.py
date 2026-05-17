from django import forms
from .models import Abitudine

class AbitudineForm(forms.ModelForm):
    class Meta:
        model = Abitudine
        fields = ['nome']
        labels = {'nome': 'Nome abitudine'}
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Es. Leggere, Bere acqua...',
                'autofocus': True,
            })
        }