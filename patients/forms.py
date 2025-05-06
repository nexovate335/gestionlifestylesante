from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nom', 'prenom', 'age','nationalite', 'sexe', 'situation_matrimoniale', 'type_personne','niveau_instruction','piece_identite', 'telephone', 'adresse', 'groupe_sanguin','numero_dossier',
        'personne_contacter','adresse_personne_contacter','telephone_personne_contacter', 'lien','medecin','assistant']
        widgets = {
            'sexe': forms.RadioSelect(choices=Patient.SEXE_CHOICES, attrs={'class': 'form-check-inline'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de famille'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le prénom'}),
            'profession': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la profession'}),
            'piece_identite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro pièce d\'identité'}),
            'niveau_instruction': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'âge'}),
            'nationalite': forms.Select(attrs={'class': 'form-select'}),
            'situation_matrimoniale': forms.Select(attrs={'class': 'form-select'}),
            'type_personne': forms.Select(attrs={'class': 'form-select'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de téléphone'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'adresse'}),
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
            'numero_dossier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de dossier'}),
            'personne_contacter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne à contacter si besoin' }),
            'adresse_personne_contacter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'adresse de la cette personne'}),
            'telephone_personne_contacter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de téléphone de cette personne'}),
            'lien': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le lien avec cette personne'}),
            'medecin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le medecin'}),
            'assistant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'assistant(e)'}),
            

        }



class PatientLabForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [ 'groupe_sanguin']
        widgets = {
            'groupe_sanguin': forms.Select(attrs={'class': 'form-select'}),
        }

