from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from personnels.models import Personnel
from patients.models import Patient
from pharmacie.models import Fournisseur 
from decimal import Decimal
import random


class PhGardeProduitManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

# Table Produits
class PhGardeProduit(models.Model):
    nom_produit = models.CharField(max_length=100, verbose_name="Nom de produit")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = PhGardeProduitManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "PhGardeProduit"
        verbose_name_plural = "PhGardeProduits"

    def __str__(self):
        return self.nom_produit

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class PhGardeCommandeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

# Table Commandes
class PhGardeCommande(models.Model):
    num_com = models.AutoField(primary_key=True)
    produit = models.ForeignKey(PhGardeProduit, on_delete=models.PROTECT, verbose_name="Produit")
    quantite_commande = models.PositiveIntegerField(verbose_name="Quantité commande")
    fournisseur = models.ForeignKey(Fournisseur,null=True, blank=True, on_delete=models.CASCADE, verbose_name="Fournisseur")
    prix = models.DecimalField(
        max_digits=10, decimal_places=2, 
        blank=True, null=True, 
        validators=[MinValueValidator(0)], 
        verbose_name="Prix d'achat unitaire"
    )
    total_achat = models.DecimalField(
        max_digits=12, decimal_places=2, 
        editable=False,  # Ne pas permettre l'édition manuelle dans le formulaire admin
        default=0, 
        verbose_name="Total achat"
    )
    date_admission = models.DateField(null=True, blank=True, verbose_name="Date d'admission")
    date_expiration = models.DateField(null=True, blank=True, verbose_name="Date d'expiration")
    date_commande = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de commande")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = PhGardeCommandeManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "PhGardeCommande"
        verbose_name_plural = "PhGardeCommandes"

    def save(self, *args, **kwargs):
        # Calcul automatique du total avant sauvegarde
        if self.prix is not None and self.quantite_commande is not None:
            self.total_achat = self.prix * self.quantite_commande
        else:
            self.total_achat = 0  # Par sécurité, si prix ou quantité manquent
        super().save(*args, **kwargs)
        self.enregistrer_reception_commande()

    def enregistrer_reception_commande(self):
        stock, created = PhGardeStock.objects.get_or_create(produit=self.produit)
        stock.quantite_reelle += self.quantite_commande
        stock.save()

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"Commande {self.num_com} - {self.produit.nom_produit}"

class PhGardeStockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

# Table Stock
class PhGardeStock(models.Model):
 
    produit = models.OneToOneField(
        'PhGardeProduit',
        on_delete=models.PROTECT,
        related_name='stock',
        verbose_name="Produit"
    )

    quantite_reelle = models.PositiveIntegerField(default=0, verbose_name="Quantité réelle")
    quantite_vendue = models.PositiveIntegerField(default=0, verbose_name="Quantité vendue")
    quantite_restante = models.PositiveIntegerField(default=0, verbose_name="Quantité restante", editable=False)

    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True, null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Prix unitaire"
    )

    prix_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True, null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Prix total"
    )

    date_stock = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de stockage")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    # Managers
    objects = PhGardeStockManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Stock de Garde"
        verbose_name_plural = "Stocks de Garde"

    def save(self, *args, **kwargs):
        if self.prix_unitaire is None:
            self.prix_unitaire = 0

        self.prix_total = self.quantite_reelle * self.prix_unitaire
        self.quantite_restante = max(self.quantite_reelle - self.quantite_vendue, 0)

        super().save(*args, **kwargs)

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"Stock de {self.produit.nom_produit}"


def generate_unique_numero_facture():
    random_number = random.randint(0,1000000)  # 5 chiffres aléatoires
    return f"PHGarde-{random_number}"


class PhGardeFacturePharmacieManager(models.Manager):
    def get_queryset(self):
        """Retourne uniquement les factures non supprimées."""
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        """Retourne uniquement les factures supprimées."""
        return super().get_queryset().filter(deleted_at__isnull=False)

    def total_avances(self, facture):
        """Calcule le total des avances effectuées pour une facture donnée."""
        return (
            self.get_queryset()
            .filter(id=facture.id)
            .aggregate(total_avances=models.Sum('total_somme_verse'))['total_avances']
            or Decimal('0.00')
        )

    def historique_paiements(self, facture):
        """Retourne l'historique des avances pour une facture donnée."""
        return facture.avances.filter(deleted_at__isnull=True).order_by('date_versement')


class PhGardeFacturePharmacie(models.Model):
    
    numero_facture = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_numero_facture, 
        verbose_name="Numéro de facture"
    )
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient",null=True, blank=True)
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    save_by = models.ForeignKey(Personnel, on_delete=models.PROTECT, verbose_name="Agent")
    facture_date_time = models.DateTimeField(auto_now_add=True, verbose_name="Date de création de la Facture") 
    
    total = models.DecimalField(
        max_digits=15, decimal_places=2, 
        validators=[MinValueValidator(0)],
        verbose_name="Total", null=True, blank=True
    )
    somme_verse = models.DecimalField(
        max_digits=15, decimal_places=2, 
        default=0.00, 
        validators=[MinValueValidator(0)],
        verbose_name="Somme versée", null=True, blank=True
    )
    avance = models.DecimalField(  # Nouveau champ pour gérer l'avance temporaire
        max_digits=15, decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name="Avance"
    )
    total_somme_verse = models.DecimalField(
        max_digits=15, decimal_places=2, 
        default=0.00, 
        validators=[MinValueValidator(0)],
        verbose_name="Total des sommes versées", null=True, blank=True
    )
    reste_a_payer = models.DecimalField(
        max_digits=15, decimal_places=2, 
        default=0.00, 
        validators=[MinValueValidator(0)],
        verbose_name="Reste à payer", null=True, blank=True
    )
    nombre_versements = models.PositiveIntegerField(default=0, verbose_name="Nombre de paiements effectués")
    
    last_updated_date = models.DateTimeField(null=True, blank=True, verbose_name="Date de dernière mise à jour")
    paye = models.BooleanField(default=False, verbose_name="Payé")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")

    objects = PhGardeFacturePharmacieManager()

    class Meta:
        verbose_name = "PhGardeFacturePharmacie"
        verbose_name_plural = "PhGardeFacturePharmacies"

    def __str__(self):
        return f"{self.numero_facture}"

    @property
    def get_total(self):
        """Calcule le total des ventes associées à cette facture."""
        ventes = self.phgardevente_set.filter(deleted_at__isnull=True)
        total = sum(vente.prix_total for vente in ventes if vente.prix_total)
        return total

    @property
    def reste(self):
        """Calcule le reste à payer."""
        total = self.total or 0  
        total_somme_verse = self.total_somme_verse or 0
        return max(total - total_somme_verse, 0)

    def save(self, *args, **kwargs):
        if self.total is None:
            self.total = 0

        # Si une somme est versée, elle est enregistrée comme une avance
        if self.somme_verse and self.somme_verse > 0:
            self.avance = self.somme_verse  # Stocke temporairement l'avance
            self.total_somme_verse += self.somme_verse

            # Historique des versements
            PhGardeFactureAvance.objects.create(facture=self, montant=self.somme_verse, date_versement=now())

            # Incrémentation du nombre de versements
            self.nombre_versements += 1
            
            # Remise à zéro de la somme_versée après enregistrement
            self.somme_verse = 0

        # Calcul du reste à payer
        self.reste_a_payer = max(self.total - Decimal(self.total_somme_verse), Decimal(0))

        # Mise à jour du statut "Payé"
        if self.total_somme_verse >= self.total:
            self.total_somme_verse = self.total
            self.paye = True
        else:
            self.paye = False

        # Date de mise à jour
        self.last_updated_date = now()

        super().save(*args, **kwargs)


class PhGardeFactureAvanceManager(models.Manager):
    """Gestionnaire personnalisé pour le modèle FactureAvance."""

    def get_queryset(self):
        """Retourne uniquement les avances non supprimées."""
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        """Retourne uniquement les avances supprimées."""
        return super().get_queryset().filter(deleted_at__isnull=False)

    def total_avances(self, facture):
        """Retourne le total des avances effectuées pour une facture donnée."""
        return (
            self.get_queryset()
            .filter(facture=facture)
            .aggregate(total=models.Sum('montant'))['total']
            or Decimal('0.00')
        )

    def historique_avances(self, facture):
        """Retourne l'historique des avances pour une facture donnée."""
        return self.get_queryset().filter(facture=facture).order_by('date_versement')



class PhGardeFactureAvance(models.Model):
    """Modèle pour enregistrer les avances sur une facture."""

    facture = models.ForeignKey(
        PhGardeFacturePharmacie, on_delete=models.CASCADE, related_name="avances", verbose_name="Numéro de Facture"
    )
    montant = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Montant versé"
    )
    date_versement = models.DateTimeField(default=now, verbose_name="Date du versement")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")  # Ajouté

    objects = PhGardeFactureAvanceManager()  # Gestionnaire pour objets actifs
    all_objects = models.Manager()  # Gestionnaire pour tous les objets

    class Meta:
        verbose_name = "PhGardeAvance"
        verbose_name_plural = "PhGardeAvances"

    def delete(self):
        """Marque l'enregistrement comme supprimé."""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """Restaure un enregistrement supprimé."""
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.facture.numero_facture}"


class PhGardeVenteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class PhGardeVente(models.Model):
    num_vente = models.AutoField(primary_key=True)
    facture = models.ForeignKey(
        'PhGardeFacturePharmacie',
        on_delete=models.PROTECT,
        verbose_name="Facture"
    )
    produit = models.ForeignKey(
        'PhGardeProduit',
        on_delete=models.PROTECT,
        related_name='ventes',
        verbose_name="Produit"
    )

    quantite_vendue = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Quantité vendue"
    )
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True, null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Prix unitaire"
    )
    prix_total = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True, null=True,
        validators=[MinValueValidator(0)],
        verbose_name="Prix total"
    )
    date_vente = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de vente")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")

    objects = PhGardeVenteManager()

    class Meta:
        verbose_name = "Vente de garde"
        verbose_name_plural = "Ventes de garde"

    def save(self, *args, **kwargs):
        stock = PhGardeStock.objects.get(produit=self.produit)

        self.prix_unitaire = stock.prix_unitaire or 0
        self.prix_total = self.quantite_vendue * self.prix_unitaire

        # Validation stock
        if stock.quantite_restante == 0:
            raise ValidationError("❌ Impossible d'effectuer la vente : le stock est vide.")

        if self.quantite_vendue > stock.quantite_restante:
            raise ValidationError(f"❌ Stock insuffisant : il ne reste que {stock.quantite_restante} unités pour ce produit.")

        if stock.quantite_restante - self.quantite_vendue < 5:
            raise ValidationError(
                f"⚠️ Attention : après cette vente, le stock deviendra critique ({stock.quantite_restante - self.quantite_vendue} unités restantes)."
            )

        # Mise à jour du stock
        stock.quantite_vendue += self.quantite_vendue
        stock.quantite_restante = stock.quantite_reelle - stock.quantite_vendue
        stock.save()

        # Sauvegarde de la vente
        super().save(*args, **kwargs)

        # Mise à jour automatique du total de la facture
        self.facture.total = self.facture.get_total
        self.facture.save()

    def delete(self):
        """Suppression logique + mise à jour facture"""
        self.deleted_at = now()
        self.save()
        self.facture.total = self.facture.get_total
        self.facture.save()

    def restore(self):
        """Restauration logique"""
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"Vente {self.num_vente}"