from django.db import models
from django_countries.fields import CountryField
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",
        blank=True
    )


class PersonnelManager(models.Manager):
    """Gestionnaire personnalisé pour le modèle Personnel."""

    def get_queryset(self):
        """Retourne uniquement les objets non supprimés."""
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        """Retourne uniquement les objets supprimés."""
        return super().get_queryset().filter(deleted_at__isnull=False)


class Personnel(models.Model):
    """Modèle Personnel avec suppression logique et synchronisation des données utilisateur."""
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    FONCTION_CHOICES = [
        ('Admin', 'Administrateur'),
        ('Info-comptable', 'Info-comptable'),
        ('Médecin', 'Médecin'),
        ('Pharmacien(ne)', 'Pharmacien(ne)'),
        ('Cassier(e)', 'Cassier(e)'),
        ('Réceptioniste', 'Réceptioniste'),
        ('Infirmier(e)', 'Infirmier(e)'),
        ('Laborantin(ne)','Laborantin(ne)'),
        ('Instrumentiste','Instrumentiste'),
        ('Penseur','Penseur'),
        ('Anesthesiste','Anesthesiste'),
        ('Aides-soignante','Aides-soignante'),
        ('Gestionnaire-phamarcie','Gestionnaire-pharmacie'),
        
        
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name="Compte utilisateur")
    first_name = models.CharField(max_length=150, verbose_name="Prénom", blank=True)
    last_name = models.CharField(max_length=150, verbose_name="Nom", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)  # Ajout du champ email
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")
    date_naissance = models.DateField(verbose_name="Date de naissance")
    lieu_naissance = models.CharField(max_length=100, verbose_name="Lieu de naissance")
    nationalite = CountryField(verbose_name="Nationalité", default='CG')
    adresse = models.TextField(verbose_name="Adresse")
    telephone = models.CharField(max_length=25, verbose_name="Téléphone")
    fonction = models.CharField(max_length=50, choices=FONCTION_CHOICES, verbose_name="Fonction")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = PersonnelManager()  # Gestionnaire pour objets actifs
    all_objects = models.Manager()  # Gestionnaire pour tous les objets

    class Meta:
        verbose_name = "Personnel"
        verbose_name_plural = "Personnels"

    def save(self, *args, **kwargs):
        """Met à jour automatiquement le prénom, nom et email de CustomUser."""
        if self.user:
            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.email = self.email  # Synchronisation de l'email
            self.user.save()
        super().save(*args, **kwargs)

    def delete(self):
        """Marque l'enregistrement comme supprimé."""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """Restaure un enregistrement supprimé."""
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.fonction}"
