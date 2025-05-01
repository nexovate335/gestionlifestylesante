from django.db import models
from django.utils.timezone import now
from patients.models import Patient


class ViolManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class Viol(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    medecin = models.CharField(max_length=100, verbose_name="Médecin")
    observation = models.TextField(verbose_name="Obseration")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")  # Date définie par défaut lors de la création
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")

    objects = ViolManager()

    class Meta:
        verbose_name = "Viol"
        verbose_name_plural = "Viols"

    def __str__(self):
        return f"{self.patient.nom} {self.patient.prenom} - Médecin: {self.medecin}"

    def delete(self):
        """Effectue une suppression logique en définissant deleted_at."""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """Restaure une instance supprimée logiquement en réinitialisant deleted_at."""
        self.deleted_at = None
        self.save()
