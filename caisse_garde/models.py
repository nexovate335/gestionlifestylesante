from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator
from patients.models import Patient
from personnels.models import Personnel
import random
from decimal import Decimal



def generate_unique_numero_facture():
    random_number = random.randint(0,1000000)  # 5 chiffres aléatoires
    return f"HO-Garde-{random_number}"

class FactureCaisseGardeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class FactureCaisseGarde(models.Model):
    numero_facture = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_numero_facture, 
        verbose_name="Numéro de facture"
    )
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient",null=True, blank=True)
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    numero_dossier = models.CharField(max_length=100, verbose_name="Numéro de dossier", null=True, blank=True)
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
    avance = models.DecimalField(
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

    class Meta:
        verbose_name = "Facture Caisse Garde"
        verbose_name_plural = "Factures Caisses Garde"

    def __str__(self):
        return f"{self.numero_facture}"

    @property
    def get_total(self):
        caisses = self.caissegarde_set.filter(deleted_at__isnull=True)
        total = sum(caisse.montant for caisse in caisses if caisse.montant)
        return total

    def save(self, *args, **kwargs):
        if self.total is None:
            self.total = 0

        if self.somme_verse and self.somme_verse > 0:
            self.avance = self.somme_verse
            self.total_somme_verse += self.somme_verse
            FactureAvanceGarde.objects.create(facture=self, montant=self.somme_verse, date_versement=now())
            self.nombre_versements += 1
            self.somme_verse = 0

        self.reste_a_payer = max(self.total - Decimal(self.total_somme_verse), Decimal(0))
        self.paye = self.total_somme_verse >= self.total
        self.last_updated_date = now()

        super().save(*args, **kwargs)


class FactureAvanceGardeManager(models.Manager):
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
        

class FactureAvanceGarde(models.Model):
    facture = models.ForeignKey(FactureCaisseGarde, on_delete=models.CASCADE, related_name="avances", verbose_name="Numéro de facture")
    montant = models.DecimalField(
        max_digits=15, decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Montant versé"
    )
    date_versement = models.DateTimeField(default=now, verbose_name="Date du versement")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")
    
    objects = FactureAvanceGardeManager()  # Gestionnaire pour objets actifs
    all_objects = models.Manager()  # Gestionnaire pour tous les objets

    class Meta:
        verbose_name = "Avance Garde"
        verbose_name_plural = "Avances Garde"
        
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


class CaisseGardeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class CaisseGarde(models.Model):

    motif = models.CharField(max_length=255,  verbose_name="Motif du paiement")
    facture = models.ForeignKey(FactureCaisseGarde, on_delete=models.PROTECT, verbose_name="Facture")
    montant = models.DecimalField(
        max_digits=10, decimal_places=2, 
        blank=True, null=True, 
        validators=[MinValueValidator(0)],
        verbose_name="Montant"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de paiement")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.facture.total = self.facture.get_total
        self.facture.save()

    def delete(self):
        self.deleted_at = now()
        self.save()
        self.facture.total = self.facture.get_total
        self.facture.save()

    def restore(self):
        self.deleted_at = None
        self.save()
        self.facture.total = self.facture.get_total
        self.facture.save()


class AutresDepensesGardeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class AutresDepensesGarde(models.Model):
    motif = models.CharField(max_length=500, verbose_name="Autres Dépenses")
    montant = models.DecimalField(
        max_digits=10, decimal_places=2, 
        null=True, blank=True, 
        validators=[MinValueValidator(0)],  # Empêche les valeurs négatives
        verbose_name="Montant"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")
    
    
    objects = AutresDepensesGardeManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "AutresDepenseGarde"
        verbose_name_plural = "AutresDepenses Garde"

    def __str__(self):
        return f"{self.motif} - {self.montant} - {self.date}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class RapportJournalierCaisseGardeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class RapportJournalierCaisseGarde(models.Model):
    caissier = models.CharField(max_length=255, verbose_name="Nom complet du caissier/caissière")
    total_encaisse = models.DecimalField(
        max_digits=12, decimal_places=2, 
        validators=[MinValueValidator(0)], 
        verbose_name="Total encaissé"
    )
    depense = models.DecimalField(
        max_digits=12, decimal_places=2, 
        validators=[MinValueValidator(0)], 
        verbose_name="Dépense"
    )
    reste = models.DecimalField(
        max_digits=12, decimal_places=2, 
        validators=[MinValueValidator(0)], 
        editable=False,
        verbose_name="Reste"
    )
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date du rapport")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = RapportJournalierCaisseGardeManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Rapport journalier de caisse garde"
        verbose_name_plural = "Rapports journaliers de caisse garde"

    def __str__(self):
        return f"Rapport - {self.caissier} - {self.date}"

    def save(self, *args, **kwargs):
        self.reste = self.total_encaisse - self.depense
        super().save(*args, **kwargs)

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()