from django import forms
from .models import Viol

class ViolForm(forms.ModelForm):
    class Meta:
        model = Viol
        fields = ['patient','nom_personne','montant', 'medecin', 'observation','commentaire']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le montant'}),
            'medecin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du médecin'}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez des observations'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),
        }
