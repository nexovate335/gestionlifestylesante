from django.db import models
from django.utils.timezone import now
from patients.models import Patient

class HospitalisationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

class Hospitalisation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    date_admission = models.DateTimeField(verbose_name="Date d'admission")
    date_sortie = models.DateTimeField(null=True, blank=True, verbose_name="Date de sortie")
    nombre_jours = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nombre de jours")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = HospitalisationManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Hospitalisation"
        verbose_name_plural = "Hospitalisations"

    def __str__(self):
        return f"{self.patient.nom} {self.patient.prenom} - Nombre de jours: {self.nombre_jours}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
