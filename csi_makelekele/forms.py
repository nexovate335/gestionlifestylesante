from django import forms
from .models import Prestation

class PrestationForm(forms.ModelForm):
    class Meta:
        model = Prestation
        fields = ['nom_complet', 'numero_dossier', 'motif', 'type', 'observation']
        widgets = {
            'nom_complet': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_dossier': forms.TextInput(attrs={'class': 'form-control'}),
            'motif': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'observation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'nom_complet': "Nom complet du patient",
            'numero_dossier': "Numéro de dossier",
            'motif': "Motif de la visite",
            'type': "Type de prestation",
            'observation': "Observation",
        }
