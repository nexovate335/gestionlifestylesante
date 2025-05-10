from django import forms
from .models import Vaccin

class VaccinForm(forms.ModelForm):
    class Meta:
        model = Vaccin
        fields = ['patient', 'nom_personne', 'type_vaccin', 'montant','commentaire']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'type_vaccin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : Pfizer, Moderna...'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le montant'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),

        }
