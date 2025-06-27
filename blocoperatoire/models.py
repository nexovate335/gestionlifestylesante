from django.db import models
from django.utils.timezone import now
from patients.models import Patient
from personnels.models import Personnel

class BlocOperatoireManager(models.Manager):
    """Gestionnaire personnalisé pour le modèle BlocOperatoire."""

    def get_queryset(self):
        """Retourne uniquement les objets non supprimés."""
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        """Retourne uniquement les objets supprimés."""
        return super().get_queryset().filter(deleted_at__isnull=False)

class BlocOperatoire(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT,null=True, blank=True, verbose_name="Patient")
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    numero_dossier = models.CharField(max_length=100, verbose_name="Numéro de dossier", null=True, blank=True)
    actes = models.CharField(max_length=255, verbose_name="Actes")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    medecin = models.CharField(max_length=100,null=True, blank=True, verbose_name="Médecin")
    aides = models.TextField(null=True, blank=True, verbose_name="Aides médecins")  # Champ texte pour stocker des informations plus longues
    instrumentiste = models.CharField(max_length=100, verbose_name="Instrumentiste", blank=True, null=True)
    panseur = models.CharField(max_length=100, verbose_name="Panseur", blank=True, null=True)
    anesthesiste = models.CharField(max_length=100, verbose_name="Anesthésiste", blank=True, null=True)
    observation = models.TextField(null=True, blank=True, verbose_name="Observation")
    save_by = models.ForeignKey(Personnel, on_delete=models.PROTECT, verbose_name="Agent", null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")  # Champ pour suppression logique

    objects = BlocOperatoireManager()  # Gestionnaire pour objets actifs
    all_objects = models.Manager()  # Gestionnaire pour tous les objets (actifs et supprimés)

    class Meta:
        verbose_name = "BlocOpératoire"
        verbose_name_plural = "BlocOpératoires"

    def delete(self):
        """Marque l'enregistrement comme supprimé."""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """Restaure un enregistrement supprimé."""
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"Actes: {self.actes}"
