from django import forms
from .models import Hospitalisation

class HospitalisationForm(forms.ModelForm):
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
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Date d\'admission', 'type': 'datetime-local'})
    )
    date_sortie = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'placeholder': 'Date de sortie', 'type': 'datetime-local'})
    )

    class Meta:
        model = Hospitalisation
        fields = ['patient', 'montant', 'nombre_jours', 'commentaire', 'date_admission', 'date_sortie']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
        }
