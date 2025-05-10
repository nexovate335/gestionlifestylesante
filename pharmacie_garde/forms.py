from django import forms
from django.forms import inlineformset_factory
from .models import PhGardeProduit, PhGardeCommande, PhGardeStock, PhGardeFacturePharmacie, PhGardeVente



class PhGardeProduitForm(forms.ModelForm):
    class Meta:
        model = PhGardeProduit
        fields = ['nom_produit']
        labels = {
            'nom_produit': 'Nom du produit',
        }
        widgets = {
            'nom_produit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du produit'}),
        }


class PhGardeCommandeForm(forms.ModelForm):
    class Meta:
        model = PhGardeCommande
        fields = [
            'produit', 'quantite_commande', 'type_produit',
            'prix', 'fournisseur', 'date_admission', 'date_expiration'
        ]
        labels = {
            'produit': 'Produit',
            'quantite_commande': 'Quantité commandée',
            'type_produit': 'Type de produit',
            'prix': 'Prix unitaire d\'achat',
            'fournisseur': 'Fournisseur',
            'date_admission': 'Date d\'admission',
            'date_expiration': 'Date d\'expiration',
        }
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez le produit'}),
            'quantite_commande': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la quantité commandée'}),
            'type_produit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le type de produit'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le prix unitaire', 'step': '0.01'}),
            'fournisseur': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez le fournisseur'}),
            'date_admission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_expiration': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PhGardeStockForm(forms.ModelForm):
    class Meta:
        model = PhGardeStock
        fields = ['produit', 'type_produit', 'quantite_reelle', 'prix_unitaire']
        labels = {
            'produit': 'Produit',
            'type_produit': 'Type de produit',
            'quantite_reelle': 'Quantité réelle',
            'prix_unitaire': 'Prix unitaire de vente',
        }
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un produit'}),
            'type_produit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le type de produit'}),
            'quantite_reelle': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la quantité réelle'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le prix unitaire', 'step': '0.01'}),
        }
        
        
class PhGardeVenteForm(forms.ModelForm):
    class Meta:
        model = PhGardeVente
        fields = ['produit', 'quantite_vendue']
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control'}),
            'quantite_vendue': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class PhGardeFacturePharmacieForm(forms.ModelForm):
    
    class Meta:
        model = PhGardeFacturePharmacie
        fields = ['patient','nom_personne']  # Ajout du champ somme versée
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            
        }

PhGardeVenteFormSet = inlineformset_factory(PhGardeFacturePharmacie, PhGardeVente, form=PhGardeVenteForm, extra=1, can_delete=False)


class PhGardeFacturePharmacieFormUpdate(forms.ModelForm):
    class Meta:
        model = PhGardeFacturePharmacie
        fields = [
            'somme_verse', 'commentaire'
        ]
