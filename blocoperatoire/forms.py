from django import forms
from .models import BlocOperatoire

class BlocOperatoireForm(forms.ModelForm):
    
    actes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Décrivez les actes opératoires', 'rows': 3})
    )
    montant = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Entrez le montant'})
    )
    medecin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du médecin'})
    )
    aides = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez les aides médecins', 'rows': 3})
    )
    instrumentiste = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'instrumentiste'})
    )
    panseur = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le panseur'})
    )
    anesthesiste = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'anesthésiste'})
    )
    observation = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ajoutez des observations', 'rows': 3})
    )
    commentaire = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ajoutez un commentaire', 'rows': 3})
    )

    class Meta:
        model = BlocOperatoire
        fields = [
            'patient','nom_personne', 'actes', 'montant', 'medecin',
            'aides', 'instrumentiste', 'panseur', 'anesthesiste', 'observation'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            
        }



class BlocOperatoireUpdateForm(forms.ModelForm):
    actes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Décrivez les actes opératoires', 'rows': 3})
    )
    montant = forms.DecimalField(
        max_digits=10, 
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Entrez le montant'})
    )
    medecin = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du médecin'})
    )
    aides = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Entrez les aides médecins', 'rows': 3})
    )
    instrumentiste = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'instrumentiste'})
    )
    panseur = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le panseur'})
    )
    anesthesiste = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez l\'anesthésiste'})
    )
    observation = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ajoutez des observations', 'rows': 3})
    )
    commentaire = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ajoutez un commentaire', 'rows': 3})
    )

    class Meta:
        model = BlocOperatoire
        fields = [
            'patient', 'actes', 'montant', 'medecin',
            'aides', 'instrumentiste', 'panseur', 'anesthesiste', 'observation'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
        }
