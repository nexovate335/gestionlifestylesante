from django import forms
from .models import Examen, ExamenCytologiePv, Resultat, ExamenCytologieEcbu

class ExamenForm(forms.ModelForm):
    examen = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Entrez la description de l'examen"})
    )
    
    class Meta:
        model = Examen
        fields = ['patient','nom_personne', 'examen', 'prix','nature_examen', 'prescripteur', 'preleveur', 'technicien', 'commentaire']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le montant'}),
            'nature_examen': forms.Select(attrs={'class': 'form-select', "placeholder": "Entrez la nature de l'examen"}),  
            'prescripteur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du prescripteur'}),
            'preleveur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du préleveur'}),
            'technicien': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du technicien'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),
        }


class ResultatForm(forms.ModelForm):
    class Meta:
        model = Resultat
        fields = ['nom_personne','examen', 'resultat','commentaire']
        widgets = {
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'examen': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, "placeholder": "Entrez l'examen"}), 
            'resultat': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, "placeholder": "Entrez le résultat"}), 
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),  
            
        }


class ExamenCytologiePvForm(forms.ModelForm):
    pv_secretion = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Entrez la sécretion"
        })
    )
    pv_couleur = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Entrez la couleur"
        })
    )
    pv_odeur = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Entrez l'odeur"
        })
    )
    cyto_ce = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Cyto CE"
        })
    )
    cyto_leuco = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Cyto Leuco"
        })
    )
    cyto_cc = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Cyto CC"
        })
    )
    cyto_levure = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Cyto Cristaux"
        })
    )
    cyto_h = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Cyto H"
        })
    )
    cyto_tv = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Cyto TV"
        })
    )
    cyto_gram = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "Cyto Gram"
        })
    )
    commentaire = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control", 
            "placeholder": "commentaire"
        })
    )

    class Meta:
        model = ExamenCytologiePv
        fields = [
            'patient',
            'nom_personne',
            'pv_secretion',
            'pv_couleur',
            'pv_odeur',
            'cyto_ce',
            'cyto_leuco',
            'cyto_cc',
            'cyto_levure',
            'cyto_h',
            'cyto_tv',
            'cyto_gram',
            'commentaire'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            
        }


class ExamenCytologieEcbuForm(forms.ModelForm):
    class Meta:
        model = ExamenCytologieEcbu
        fields = [
            'patient',
            'nom_personne',
            'ecbu_culot',
            'ecbu_couleur',
            'cyto_ce',
            'cyto_leuco',
            'cyto_cylendre',
            'cyto_cristaux',
            'cyto_h',
            'cyto_gram',
            'commentaire'
        ]
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'ecbu_culot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le culot'}),
            'ecbu_couleur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la couleur'}),
            'cyto_ce': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cyto CE'}),
            'cyto_leuco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cyto Leuco'}),
            'cyto_cylendre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cyto Cylindre'}),
            'cyto_cristaux': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cyto Cristaux'}),
            'cyto_h': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cyto H'}),
            'cyto_gram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cyto Gram'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Entrez un commentaire'}),
        }