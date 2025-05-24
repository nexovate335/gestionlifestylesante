from django.db import models
from django.utils.timezone import now
from patients.models import Patient
from personnels.models import Personnel


class EchographieManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

class Echographie(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient",null=True, blank=True)
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    demandeur = models.CharField(max_length=100, null=True, blank=True, verbose_name="Demandeur")
    pratiqueur = models.CharField(max_length=100, null=True, blank=True, verbose_name="Pratiqueur")
    assistant = models.CharField(max_length=100, null=True, blank=True, verbose_name="Assistant(e)")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    resultat = models.TextField(null=True, blank=True, verbose_name="Résultat")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    save_by = models.ForeignKey(Personnel, on_delete=models.PROTECT, verbose_name="Agent", null=True,blank=True) 
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")
    

    objects = EchographieManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Echographie"
        verbose_name_plural = "Echographies"

    def __str__(self):
        return f"{self.id}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
