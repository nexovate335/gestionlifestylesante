from django import forms
from .models import Mto

class MtoForm(forms.ModelForm):
    demandeur = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du demandeur'})
    )
    pratiqueur = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du pratiqueur'})
    )
    assistant = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de l\'assistant(e)'})
    )
    montant = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Entrez le montant'})
    )
    resultat = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez le résultat'})
    )
    commentaire = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez le commentaire'})
    )


    class Meta:
        model = Mto
        fields = ['patient', 'demandeur', 'pratiqueur', 'assistant', 'montant', 'resultat', 'commentaire']  # Liste des champs à inclure
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),  # Sélection du patient
        }
