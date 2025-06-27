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
            'produit', 'quantite_commande',
            'prix', 'fournisseur', 'date_admission', 'date_expiration'
        ]
        labels = {
            'produit': 'Produit',
            'quantite_commande': 'Quantité commandée',
            'prix': 'Prix unitaire d\'achat',
            'fournisseur': 'Fournisseur',
            'date_admission': 'Date d\'admission',
            'date_expiration': 'Date d\'expiration',
        }
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez le produit'}),
            'quantite_commande': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la quantité commandée'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le prix unitaire', 'step': '0.01'}),
            'fournisseur': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez le fournisseur'}),
            'date_admission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_expiration': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class PhGardeStockForm(forms.ModelForm):
    class Meta:
        model = PhGardeStock
        fields = ['produit', 'quantite_reelle', 'prix_unitaire']
        labels = {
            'quantite_reelle': 'Quantité réelle',
            'prix_unitaire': 'Prix unitaire de vente',
        }
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un produit'}),
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

    def clean(self):
        cleaned_data = super().clean()
        produit = cleaned_data.get('produit')
        quantite = cleaned_data.get('quantite_vendue')

        if produit and quantite:
            try:
                stock = PhGardeStock.objects.get(produit=produit)
            except PhGardeStock.DoesNotExist:
                self.add_error('produit', "⚠️ Ce produit n’a pas de stock enregistré.")
                return cleaned_data

            if stock.quantite_restante == 0:
                self.add_error('quantite_vendue', f"❌ Stock vide pour {produit}. Vente impossible.")
            elif quantite > stock.quantite_restante:
                self.add_error(
                    'quantite_vendue',
                    f"⚠️ Quantité demandée ({quantite}) > stock disponible ({stock.quantite_restante}). Vente non autorisée."
                )
            elif stock.quantite_restante - quantite < 0:
                self.add_error(
                    'quantite_vendue',
                    f"⚠️ Attention : après cette vente, le stock sera critique ({stock.quantite_restante - quantite} unité(s))."
                )

        return cleaned_data


class PhGardeFacturePharmacieForm(forms.ModelForm):
    
    class Meta:
        model = PhGardeFacturePharmacie
        fields = ['nom_personne', 'numero_dossier']  # Ajout du champ somme versée
        widgets = {
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'numero_dossier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numero de dossier'}),
            
        }

PhGardeVenteFormSet = inlineformset_factory(PhGardeFacturePharmacie, PhGardeVente, form=PhGardeVenteForm, extra=1, can_delete=False)


class PhGardeFacturePharmacieFormUpdate(forms.ModelForm):
    class Meta:
        model = PhGardeFacturePharmacie
        fields = [
            'somme_verse', 'commentaire'
        ]
