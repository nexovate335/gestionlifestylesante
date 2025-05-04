from django import forms
from django.forms import inlineformset_factory
from django.forms import formset_factory
from .models import FactureCaisseGarde, CaisseGarde, AutresDepensesGarde, RapportJournalierCaisseGarde
from patients.models import Patient


class CaisseGardeForm(forms.ModelForm):
    class Meta:
        model = CaisseGarde
        fields = ['motif', 'montant']
        widgets = {
            'motif': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class FactureCaisseGardeForm(forms.ModelForm):
    
    class Meta:
        model = FactureCaisseGarde
        fields = ['patient']  # Ajout du champ somme versée
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
        }

CaisseFormSet = inlineformset_factory(FactureCaisseGarde, CaisseGarde, form=CaisseGardeForm, extra=1, can_delete=False)


class FactureCaisseGardeFormUpdate(forms.ModelForm):
    class Meta:
        model = FactureCaisseGarde
        fields = [
            'somme_verse', 'commentaire'
        ]


class AutresDepensesGardeForm(forms.ModelForm):
    class Meta:
        model = AutresDepensesGarde
        fields = ['motif', 'montant']
        widgets = {
            'motif': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class RapportJournalierCaisseGardeForm(forms.ModelForm):
    class Meta:
        model = RapportJournalierCaisseGarde
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
 