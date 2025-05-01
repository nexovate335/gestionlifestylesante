from django import forms
from .models import Vaccin

class VaccinForm(forms.ModelForm):
    class Meta:
        model = Vaccin
        fields = ['patient',  'type_vaccin', 'montant','commentaire']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'type_vaccin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : Pfizer, Moderna...'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le montant'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),

        }
