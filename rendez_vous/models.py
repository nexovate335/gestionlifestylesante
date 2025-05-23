from django.db import models
from django.utils.timezone import now
from personnels.models import Personnel
import calendar

class RendezVousManager(models.Manager):
    def get_queryset(self):
        """ Récupère uniquement les rendez-vous non supprimés (deleted_at est NULL). """
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        """ Récupère uniquement les rendez-vous supprimés (deleted_at n'est pas NULL). """
        return super().get_queryset().filter(deleted_at__isnull=False)

class RendezVous(models.Model):
    nom_docteur = models.CharField(max_length=200, verbose_name="Nom du Docteur")
    nom_personne = models.CharField(max_length=255, verbose_name="Nom complet de la personne concernée")

    jour_rdv = models.PositiveIntegerField()

    MOIS_CHOICES = [
        (1, 'Janvier'),
        (2, 'Février'),
        (3, 'Mars'),
        (4, 'Avril'),
        (5, 'Mai'),
        (6, 'Juin'),
        (7, 'Juillet'),
        (8, 'Août'),
        (9, 'Septembre'),
        (10, 'Octobre'),
        (11, 'Novembre'),
        (12, 'Décembre'),
    ]
    
    mois_rdv = models.PositiveSmallIntegerField(
        choices=MOIS_CHOICES,
        default=1,
        verbose_name="Mois du rendez-vous"
    )
    annee_rdv = models.PositiveSmallIntegerField(default=2025, verbose_name="Année du rendez-vous")

    heure_rdv = models.TimeField(verbose_name="Heure du rendez-vous")

    STATUT_CHOICES = [
        ('confirmé', 'Confirmé'),
        ('annulé', 'Annulé'),
        ('en_attente', 'En attente'),
    ]
    statut = models.CharField(max_length=15, choices=STATUT_CHOICES, default='en_attente', verbose_name="Statut du rendez-vous")

    numero_dossier = models.CharField(max_length=100, null=True, blank=True, verbose_name="Numéro du dossier")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")

    acte = models.BooleanField(default=False, verbose_name="Actes réalisés ou prévus")  # Passage en booléen
    
    save_by = models.ForeignKey(Personnel, on_delete=models.PROTECT, verbose_name="Agent", null=True,blank=True) 
    
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de suppression")

    objects = RendezVousManager()  # Gestionnaire pour les rendez-vous actifs
    all_objects = models.Manager()  # Gestionnaire pour TOUS les rendez-vous (actifs et supprimés)

    class Meta:
        verbose_name = "Rendez-vous"
        verbose_name_plural = "Rendez-vous"

    def __str__(self):
        return f"Rendez-vous avec {self.nom_docteur} pour {self.nom_personne} le {self.jour_rdv}/{self.mois_rdv}/{self.annee_rdv} à {self.heure_rdv}"

    def save(self, *args, **kwargs):
        """ Calcule le jour de la semaine à partir des valeurs jour/mois/année. """
        try:
            self.jour_semaine = calendar.day_name[calendar.weekday(self.annee_rdv, self.mois_rdv, self.jour_rdv)]
        except ValueError:
            self.jour_semaine = "Invalide"  # Pour éviter les erreurs si la date est incorrecte
        super().save(*args, **kwargs)

    def delete(self):
        """ Effectue une suppression logique en définissant deleted_at. """
        self.deleted_at = now()
        self.save()

    def restore(self):
        """ Restaure un rendez-vous supprimé logiquement. """
        self.deleted_at = None
        self.save()
