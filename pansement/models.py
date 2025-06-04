from django.db import models
from django.utils.timezone import now
from patients.models import Patient
from personnels.models import Personnel


class PansementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

class Pansement(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient")
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    panseur = models.CharField(max_length=100, null=True, blank=True, verbose_name="Panseur")
    observation = models.TextField(verbose_name="Obseration")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    save_by = models.ForeignKey(Personnel, on_delete=models.PROTECT, verbose_name="Agent", null=True,blank=True)  
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")
    
    objects = PansementManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Pansement"
        verbose_name_plural = "Pansements"

    def __str__(self):
        return f"{self.patient.nom} {self.patient.prenom} - Médecin: {self.panseur}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
