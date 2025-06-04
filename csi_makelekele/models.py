from django.db import models
from django.utils.timezone import now


class PrestationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class Prestation(models.Model):
    nom_complet = models.CharField(max_length=255, verbose_name="Nom complet du patient")
    numero_dossier = models.CharField(max_length=100, verbose_name="Numéro de dossier")
    motif = models.CharField(max_length=255, verbose_name="Motif de la visite")
    type = models.CharField(max_length=100, verbose_name="Type de prestation")
    observation = models.TextField(blank=True, null=True, verbose_name="Observation")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = PrestationManager()  # Prestations actives
    all_objects = models.Manager()  # Toutes prestations (y compris supprimées)

    class Meta:
        verbose_name = "Prestation"
        verbose_name_plural = "Prestations"

    def __str__(self):
        return f"{self.nom_complet} - {self.type} ({self.date.date()})"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
