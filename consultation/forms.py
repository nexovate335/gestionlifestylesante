from django import forms
from django.forms import inlineformset_factory
from .models import Consultation, Ordonnance, Traitement

from django import forms
from .models import Consultation

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [
           'nom_personne','numero_dossier', 'type_consultation','montant', 'medecin', 'assistant', 'commentaire',
        ]

        widgets = {
            'nom_personne': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_dossier': forms.TextInput(attrs={'class': 'form-control'}),
            'type_consultation': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Montant à payer'}),
            'medecin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du médecin'}),
            'assistant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Nom de l'assistant(e)"}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Commentaire'}),
        }


class SuiteConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [ 
            'motif_consultation',
            'temperature', 'tension_arterielle', 'pouls', 'saturation', 'poids', 'taille', 'imc',
            'tdr', 'glycemie', 'alb_sucre',
            'atcd_socioeconomique', 'atcd_chomage', 'atcd_violence_domestique', 'atcd_prison',
            'atcd_arret_ecole', 'atcd_victime_guerre',
        ]

        widgets = {
            'motif_consultation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Motif de la consultation'}),

            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '°C'}),
            'tension_arterielle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 12/8'}),
            'pouls': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'bpm'}),
            'saturation': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '%'}),
            'poids': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'kg'}),
            'taille': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'm'}),
            'imc': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Calculé ou saisi'}),

            'tdr': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'glycemie': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mg/dL'}),
            'alb_sucre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Si grossesse'}),

            'atcd_socioeconomique': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'atcd_chomage': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'atcd_violence_domestique': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'atcd_prison': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'atcd_arret_ecole': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'atcd_victime_guerre': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        


class SuiviConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [
            'suivi_medecin',
            'commentaire'
        ]

        widgets = {
            'suivi_medecin': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Évolution ou recommandations'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Commentaire'}),
           
        }


class OrdonnanceForm(forms.ModelForm):
    class Meta:
        model = Ordonnance
        exclude = ['deleted_at', 'date']  # Exclusion des champs gérés automatiquement
        widgets = {
            'consultation': forms.Select(attrs={
                'class': 'form-control',
            }),
            'prescripteur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du prescripteur',
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Commentaires éventuels...',
            }),
        }

class TraitementForm(forms.ModelForm):
    class Meta:
        model = Traitement
        exclude = ['deleted_at', 'ordonnance', 'date_prescription']  # Champs exclus car automatiques ou injectés dans la vue
        widgets = {
            'medicament': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Nom du médicament',
            }),
            'posologie': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex. 1 comprimé matin et soir',
            }),
            'duree': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex. 7 jours',
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Commentaire (optionnel)',
            }),
        }

TraitementFormSet = inlineformset_factory(
    Ordonnance,
    Traitement,
    form=TraitementForm,
    extra=1,
    can_delete=False
)