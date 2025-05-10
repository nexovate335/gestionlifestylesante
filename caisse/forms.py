from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from .models import FactureCaisse, Caisse, AutresDepenses, RapportJournalierCaisse
from patients.models import Patient


class CaisseForm(forms.ModelForm):
    class Meta:
        model = Caisse
        fields = ['motif', 'montant']
        widgets = {
            'motif': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class FactureCaisseForm(forms.ModelForm):
    
    class Meta:
        model = FactureCaisse
        fields = ['patient','nom_personne']  # Ajout du champ somme versée
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            
        }

CaisseFormSet = inlineformset_factory(FactureCaisse, Caisse, form=CaisseForm, extra=1, can_delete=False)


class FactureCaisseFormUpdate(forms.ModelForm):
    class Meta:
        model = FactureCaisse
        fields = [
            'somme_verse', 'commentaire'
        ]


class AutresDepensesForm(forms.ModelForm):
    class Meta:
        model = AutresDepenses
        fields = ['motif', 'montant']
        widgets = {
            'motif': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class RapportJournalierCaisseForm(forms.ModelForm):
    class Meta:
        model = RapportJournalierCaisse
        fields = ['total_encaisse', 'depense']
        widgets = {
            'total_encaisse': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
            'depense': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.01'
            }),
        }
 