from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Personnel

@receiver(post_save, sender=CustomUser)
def create_personnel(sender, instance, created, **kwargs):
    if created:  # Vérifie si l'utilisateur vient d'être créé
        Personnel.objects.create(
            user=instance,
            last_name = 'lifestyle sante',
            first_name = 'lifestyle sante',
            sexe='M',  # Valeur par défaut, modifiable après
            date_naissance="2000-01-01",  # Valeur par défaut
            lieu_naissance="Non défini",
            nationalite="CG",  # Code par défaut (Congo), modifiable
            adresse="Non défini",
            telephone="000000000",
            fonction="Aucune fonction"  # Fonction par défaut, modifiable ensuite
        )
