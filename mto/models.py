from django.db import models
from django.utils.timezone import now
from patients.models import Patient

class MtoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

class Mto(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient",null=True, blank=True)
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    demandeur = models.CharField(max_length=100, null=True, blank=True, verbose_name="Demandeur")
    pratiqueur = models.CharField(max_length=100, null=True, blank=True, verbose_name="Pratiqueur")
    assistant = models.CharField(max_length=100, null=True, blank=True, verbose_name="Assistant(e)")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    resultat = models.TextField(null=True, blank=True, verbose_name="Résultat") 
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire") 
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")

    objects = MtoManager()

    class Meta:
        verbose_name = "Mto"
        verbose_name_plural = "Mto"

    def __str__(self):
        return f"{self.patient.nom} {self.patient.prenom} - Pratiqueur: {self.pratiqueur}"

    def delete(self):
        """Effectue une suppression logique en définissant deleted_at."""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """Restaure une instance supprimée logiquement en réinitialisant deleted_at."""
        self.deleted_at = None
        self.save()
