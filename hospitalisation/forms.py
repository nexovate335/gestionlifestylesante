from django import forms
from .models import Hospitalisation

class HospitalisationForm(forms.ModelForm):
    

    nom_personne = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet de la personne'}),
        label='Nom de la personne'
    )
    numero_dossier = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de dossier'}),
        label='Numéro de dossier'
    )

    montant = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le montant'})
    )

    nombre_jours = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nombre de jours'})
    )

    commentaire = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez le commentaire', 'rows': 4})
    )

    date_admission = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Date d\'admission',
            'type': 'datetime-local'
        })
    )

    date_sortie = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control',
            'placeholder': 'Date de sortie',
            'type': 'datetime-local'
        })
    )

    class Meta:
        model = Hospitalisation
        fields = [ 'nom_personne','numero_dossier', 'montant', 'nombre_jours', 'commentaire', 'date_admission', 'date_sortie']
