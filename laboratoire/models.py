from django.db import models
from django.utils.timezone import now
from patients.models import Patient

class ExamenManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class Examen(models.Model):

    NATURE_EXAMEN_CHOICES = [
        ('Examen fait maison', 'Examen fait maison'),
        ('Examen fait à l\'extérieur', 'Examen fait à l\'extérieur'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT,null=True, blank=True, verbose_name="Patient")
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    examen = models.CharField(max_length=255,verbose_name="Examen")
    prix = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")
    nature_examen = models.CharField(max_length=50,null=True, blank=True, choices=NATURE_EXAMEN_CHOICES, verbose_name="Nature de l'examen ")
    prescripteur = models.CharField(max_length=100, null=True, blank=True, verbose_name="Prescripteur")
    preleveur = models.CharField(max_length=100, null=True, blank=True, verbose_name="Préleveur")
    technicien = models.CharField(max_length=100, null=True, blank=True, verbose_name="Technicien(ne)")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")
    

    objects = ExamenManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Examen"
        verbose_name_plural = "Examens"

    def __str__(self):
        return f"Examen: {self.examen}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
        

class ResultatManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class Resultat(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT,null=True, blank=True, verbose_name="Patient")
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    examen = models.TextField(verbose_name="Examen")
    resultat = models.TextField(verbose_name="Résultat")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")
    

    objects = ResultatManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Resultat"
        verbose_name_plural = "Resultats"

    def __str__(self):
        return f"{self.examen}-{self.resultat} "

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class ExamenCytologiePvManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class ExamenCytologiePv(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT,null=True, blank=True, verbose_name="Patient")
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    pv_secretion = models.CharField(max_length=255, verbose_name="PV Sécrétion")
    pv_couleur = models.CharField(max_length=255, verbose_name="PV Couleur")
    pv_odeur = models.CharField(max_length=255, verbose_name="PV Odeur")
    cyto_ce =  models.CharField(max_length=255, verbose_name="Cyto CE")
    cyto_leuco =  models.CharField(max_length=255, verbose_name="Cyto Leuco")
    cyto_cc =  models.CharField(max_length=255, verbose_name="Cyto CC")
    cyto_levure =  models.CharField(max_length=255, verbose_name="Cyto levure")
    cyto_h =  models.CharField(max_length=255, verbose_name="Cyto H")
    cyto_tv =  models.CharField(max_length=255, verbose_name="Cyto TV")
    cyto_gram =  models.CharField(max_length=255, verbose_name="Cyto Gram")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")
    

    objects = ExamenCytologiePvManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "ExamenCytologiePv"
        verbose_name_plural = "ExamensCytologiePv"

    def __str__(self):
        return f"{self.id}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class ExamenCytologieEcbuManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class ExamenCytologieEcbu(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Patient")
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    ecbu_culot = models.CharField(max_length=255, verbose_name="ECBU Culot")
    ecbu_couleur = models.CharField(max_length=255, verbose_name="ECBU couleur")
    cyto_ce =  models.CharField(max_length=255, verbose_name="Cyto CE")
    cyto_leuco =  models.CharField(max_length=255, verbose_name="Cyto Leuco")
    cyto_cylendre =  models.CharField(max_length=255, verbose_name="Cyto Cylendre")
    cyto_cristaux =  models.CharField(max_length=255, verbose_name="Cyto Cristaux")
    cyto_h =  models.CharField(max_length=255, verbose_name="Cyto H")
    cyto_gram =  models.CharField(max_length=255, verbose_name="Cyto Gram")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")
    

    objects = ExamenCytologieEcbuManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "ExamenCytologieEcbu"
        verbose_name_plural = "ExamensCytologieEcbu"

    def __str__(self):
        return f"{self.id}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
