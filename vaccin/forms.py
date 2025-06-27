from django import forms
from .models import Vaccin

class VaccinForm(forms.ModelForm):
    class Meta:
        model = Vaccin
        fields = ['nom_personne', 'numero_dossier', 'type_vaccin', 'montant','commentaire']
        widgets = {
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'numero_dossier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de dossier'}),
            'type_vaccin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex : Pfizer, Moderna...'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le montant'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),

        }
