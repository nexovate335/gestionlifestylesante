from django import forms
from .models import RendezVous

class RendezVousForm(forms.ModelForm):
    class Meta:
        model = RendezVous
        fields = [
            'nom_personne', 'numero_dossier', 'nom_docteur', 'jour_rdv', 'mois_rdv', 'annee_rdv', 
            'heure_rdv', 'statut',  'commentaire', 'acte'
        ]
        widgets = {
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'numero_dossier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de dossier'}),
            'nom_docteur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du médecin'}),
            'jour_rdv': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le jour du rendez-vous'}),
            'mois_rdv': forms.Select(attrs={'class': 'form-select'}),
            'annee_rdv': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'année du rendez-vous'}),
            'heure_rdv': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),
            'acte': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

