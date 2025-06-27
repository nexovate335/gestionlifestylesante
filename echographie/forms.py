from django import forms
from .models import Echographie

class EchographieForm(forms.ModelForm):
    numero_dossier = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de dossier'})
    )
    demandeur = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du demandeur'})
    )
    pratiqueur = forms.CharField(
        max_length=100,
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
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez le résultat', 'rows': 3})
    )
    commentaire = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez le commentaire', 'rows': 3})
    )
    
    class Meta:
        model = Echographie
        fields = ['nom_personne','numero_dossier', 'demandeur', 'pratiqueur', 'assistant', 'montant', 'resultat', 'commentaire']
        widgets = {
           
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            
            
        }
