from django.db import models
from django_countries.fields import CountryField
from django.utils.timezone import now
import random



def generate_unique_dossier():
    random_number = random.randint(0,20000)  # 5 chiffres aléatoires
    return f"{random_number}"

class PatientManager(models.Manager):
    """Gestionnaire personnalisé pour le modèle Patient."""

    def get_queryset(self):
        """Retourne uniquement les objets non supprimés."""
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        """Retourne uniquement les objets supprimés."""
        return super().get_queryset().filter(deleted_at__isnull=False)

class Patient(models.Model):
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    SITUATION_MATRIMONIALE_CHOICES = [
        ('C', 'Célibataire'),
        ('M', 'Marié(e)'),
        ('D', 'Divorcé(e)'),
        ('V', 'Veuf/Veuve'),
        ('S', 'Séparé(e)'),
    ]

    TYPE_PERSONNE_CHOICES = [
        ('adulte', 'Adulte'),
        ('enfant', 'Enfant'),
        ('nouveau-né', 'Nouveau-né'),
    ]

    GROUPE_SANGUIN_CHOICES = [
        ('Neutre', 'Neutre'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    
    NIVEAU_INSTRUCTION_CHOICES = [
        ('Illttré(e)', 'Illetré(e)'),
        ('Primaire', 'Primaire'),
        ('Secondaire', 'Secondaire'),
        ('Universitaire', 'Universitaire'),
    ]

    numero_dossier = models.CharField(
        max_length=25,
        unique=True,
        default=generate_unique_dossier, 
        verbose_name="Numéro de dossier"
    )
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    profession = models.CharField(max_length=100, verbose_name="Profession",null=True,blank=True)
    age = models.PositiveIntegerField(verbose_name="Âge")
    nationalite = CountryField(verbose_name="Nationalité", default='CG')
    piece_identite = models.CharField(max_length=100,null=True, blank=True, verbose_name="Pièce d'identité n°")
    niveau_instruction =  models.CharField(
        max_length=50,
        choices=NIVEAU_INSTRUCTION_CHOICES,null=True, blank=True,
        verbose_name="Niveau d'instruction"
    )
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")
    situation_matrimoniale = models.CharField(
        max_length=1,
        choices=SITUATION_MATRIMONIALE_CHOICES,
        verbose_name="Situation matrimoniale"
    )
    type_personne = models.CharField(
        max_length=10,
        choices=TYPE_PERSONNE_CHOICES,
        verbose_name="Type de personne"
    )
    groupe_sanguin = models.CharField(
        max_length=15, 
        choices=GROUPE_SANGUIN_CHOICES, 
        null=True, 
        blank=True, 
        verbose_name="Groupe sanguin"
    )
    adresse = models.TextField(null=True, blank=True, verbose_name="Adresse")
    telephone = models.CharField(max_length=25, null=True,blank=True, verbose_name="Téléphone")
    personne_contacter = models.CharField(max_length=255,null=True, blank=True, verbose_name="Personne à contacter si besoin")
    adresse_personne_contacter = models.TextField(null=True, blank=True, verbose_name="Adresse personne à contacter si besoin")
    telephone_personne_contacter = models.CharField(max_length=25, null=True,blank=True, verbose_name="Téléphone personne à contacter si besoin")
    lien = models.CharField(max_length=255, null=True, blank=True, verbose_name="Lien")
    medecin = models.CharField(max_length=255, null=True, blank=True, verbose_name="Médecin" )
    assistant = models.CharField(max_length=255, null=True, blank=True, verbose_name="Assistant(e)" )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")  # Champ pour suppression logique

    objects = PatientManager()  # Gestionnaire pour objets actifs
    all_objects = models.Manager()  # Gestionnv aire pour tous les objets (actifs et supprimés)

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def delete(self):
        """Marque l'enregistrement comme supprimé."""
        self.deleted_at = now()
        self.save()

    def restore(self):
        """Restaure un enregistrement supprimé."""
        self.deleted_at = None
        self.save()

    def __str__(self):
        return f"{self.numero_dossier}-{self.nom}"
