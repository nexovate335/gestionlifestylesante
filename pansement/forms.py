from django import forms
from .models import Pansement

class PansementForm(forms.ModelForm):
    class Meta:
        model = Pansement
        fields = ['nom_personne', 'montant', 'panseur', 'observation', 'commentaire']
        widgets = {
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le montant'}),
            'panseur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du médecin'}),
            'observation': forms.Textarea(attrs={'class': 'form-control','rows': 4, 'placeholder': 'Ajoutez des observations'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),
        }
        

