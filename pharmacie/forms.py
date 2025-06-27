from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import Produit, Fournisseur, Commande, Stock, FacturePharmacie, Vente

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom_produit']
        labels = {
            'nom_produit': 'Nom du produit',
        }
        widgets = {
            'nom_produit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du produit'}),
        }

class FournisseurForm(forms.ModelForm):
    class Meta:
        model = Fournisseur
        fields = ['nom_fournisseur', 'ville', 'telephone']
        labels = {
            'nom_fournisseur': 'Nom du fournisseur',
            'ville': 'Ville',
            'telephone': 'Téléphone',
        }
        widgets = {
            'nom_fournisseur': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom du fournisseur'}),
            'ville': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la ville du fournisseur'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le téléphone du fournisseur'}),
        }

class CommandeForm(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['produit', 'quantite_commande', 'prix', 'fournisseur', 'date_admission', 'date_expiration']
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
            # Champs date avec format de date adapté
            'date_admission': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez la date d\'admission', 'type': 'date'}),
            'date_expiration': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez la date d\'expiration', 'type': 'date'}),
        }


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['produit', 'quantite_reelle', 'prix_unitaire']
        labels = {
            'produit': 'Produit',
            'quantite_reelle': 'Quantité réelle',
            'prix_unitaire': 'Prix unitaire de vente',
        }
        widgets = {
            'produit': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Sélectionnez un produit'}),
            'quantite_reelle': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez la quantité réelle'}),
            'prix_unitaire': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le prix unitaire', 'step': '0.01'}),
        }
        
        
class VenteForm(forms.ModelForm):
    class Meta:
        model = Vente
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
                stock = Stock.objects.get(produit=produit)
            except Stock.DoesNotExist:
                self.add_error('produit', "⚠️ Ce produit n'a pas de stock associé.")
                return cleaned_data

            if stock.quantite_restante == 0:
                # ❌ Blocage si stock totalement vide
                self.add_error('quantite_vendue', f"❌ Stock vide pour {produit}. Impossible d'effectuer la vente.")
            else:
                # Avertissements informatifs
                if quantite > stock.quantite_restante:
                    self.add_error(
                        'quantite_vendue',
                        f"⚠️ La quantité demandée ({quantite}) dépasse le stock disponible ({stock.quantite_restante}). La vente est quand même autorisée."
                    )
                elif stock.quantite_restante - quantite < 0:
                    self.add_error(
                        'quantite_vendue',
                        f"⚠️ Attention : après cette vente, il ne restera que {stock.quantite_restante - quantite} unité(s)."
                    )

        return cleaned_data



class FacturePharmacieForm(forms.ModelForm):
    
    class Meta:
        model = FacturePharmacie
        fields = ['nom_personne','numero_dossier']  # Ajout du champ somme versée
        widgets = {
           
            'nom_personne': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nom de la personne'}),
            'numero_dossier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le numéro de dossier'}),
            
        }

VenteFormSet = inlineformset_factory(FacturePharmacie, Vente, form=VenteForm, extra=1, can_delete=False)


class FacturePharmacieFormUpdate(forms.ModelForm):
    class Meta:
        model = FacturePharmacie
        fields = [
            'somme_verse', 'commentaire'
        ]
