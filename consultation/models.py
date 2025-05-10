from django.db import models
from django.utils.timezone import now
from patients.models import Patient

class ConsultationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)

class Consultation(models.Model):
    BLOCS = [
        ('consultation simple', 'Consultation Simple'),
        ('consultation prénatale', 'Consultation Prénatale'),
        ('consultation ORM', 'Consultation ORL'),
    ]

    type_consultation = models.CharField(max_length=100, choices=BLOCS, null=True, blank=True, verbose_name="Type de consultation")
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name="Patient")
    nom_personne = models.CharField(max_length=255,null=True, blank=True, verbose_name="Nom complet de la personne concernée")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")

    # Champs personnels
    medecin = models.CharField(max_length=100, null=True, blank=True, verbose_name="Médecin traitant")
    assistant = models.CharField(max_length=100, null=True, blank=True, verbose_name="Assistant(e)")
    commentaire = models.TextField(null=True, max_length=1000, blank=True, verbose_name="Commentaire")
    motif_consultation = models.TextField(null=True, blank=True, verbose_name="Motif de consultation")

    # Signes vitaux
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="Température (°C)")
    tension_arterielle = models.CharField(max_length=20, null=True, blank=True, verbose_name="TA (Tension artérielle)")
    pouls = models.PositiveIntegerField(null=True, blank=True, verbose_name="Pouls (bpm)")
    saturation = models.PositiveIntegerField(null=True, blank=True, verbose_name="Saturation (%)")
    poids = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Poids (kg)")
    taille = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name="Taille (m)")
    imc = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="IMC")

    # Bilan préliminaire de routine
    tdr = models.BooleanField(default=False, verbose_name="TDR positif (si fièvre)")
    glycemie = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Glycémie")
    alb_sucre = models.CharField(max_length=50, null=True, blank=True, verbose_name="Alb/Sucre (si grossesse)")

    # Antécédents (ATCD)
    atcd_socioeconomique = models.BooleanField(default=False, verbose_name="Situation socioéconomique difficile")
    atcd_chomage = models.BooleanField(default=False, verbose_name="Chômage")
    atcd_violence_domestique = models.BooleanField(default=False, verbose_name="Violence domestique")
    atcd_prison = models.BooleanField(default=False, verbose_name="Passage en prison")
    atcd_arret_ecole = models.BooleanField(default=False, verbose_name="Arrêt de la scolarisation")
    atcd_victime_guerre = models.BooleanField(default=False, verbose_name="Victime de guerre")
    suivi_medecin = models.TextField(null=True, blank=True, verbose_name="Suivi du médecin")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = ConsultationManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"

    def __str__(self):
        return f"{self.patient.nom} {self.patient.prenom} {self.patient.numero_dossier} - numero de consultation: {self.id}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class OrdonnanceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class TraitementManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def deleted(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class Ordonnance(models.Model):
    consultation = models.ForeignKey(
        'Consultation',
        on_delete=models.CASCADE,
        related_name='ordonnances',
        verbose_name="Consultation liée"
    )
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    commentaire = models.TextField(null=True, blank=True, verbose_name="Commentaire général")
    prescripteur = models.CharField(max_length=100, null=True, blank=True, verbose_name="Prescripteur")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = OrdonnanceManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Ordonnance"
        verbose_name_plural = "Ordonnances"

    def __str__(self):
        return f"Ordonnance de {self.consultation.patient.nom} {self.consultation.patient.numero_dossier}"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()


class Traitement(models.Model):
    ordonnance = models.ForeignKey(
        Ordonnance,
        on_delete=models.CASCADE,
        related_name='traitements',
        verbose_name="Ordonnance liée"
    )
    medicament = models.TextField(verbose_name="Nom du médicament")
    posologie = models.CharField(max_length=200, verbose_name="Posologie")
    duree = models.CharField(max_length=100, verbose_name="Durée du traitement")
    commentaire = models.TextField(null=True, blank=True, verbose_name="Commentaire")
    date_prescription = models.DateTimeField(auto_now_add=True, verbose_name="Date de prescription")
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Supprimé le")

    objects = TraitementManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Traitement"
        verbose_name_plural = "Traitements"

    def delete(self):
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()
