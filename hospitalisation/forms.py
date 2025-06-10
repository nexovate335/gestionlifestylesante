from django import forms
from .models import Hospitalisation

class HospitalisationForm(forms.ModelForm):
    
    patient = forms.ModelChoiceField(
        queryset=Hospitalisation._meta.get_field('patient').related_model.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Patient'
    )

    nom_personne = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom complet de la personne'}),
        label='Nom de la personne'
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
        fields = ['patient', 'nom_personne', 'montant', 'nombre_jours', 'commentaire', 'date_admission', 'date_sortie']
