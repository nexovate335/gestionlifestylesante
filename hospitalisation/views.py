from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.utils.timezone import now
from .models import Hospitalisation
from .forms import HospitalisationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from personnels.mixins import SaveByPersonnelMixin

# Liste des hospitalisations actives
class HospitalisationListView(ListView):
    model = Hospitalisation
    template_name = "hospitalisation/hospitalisations/hospitalisation_list.html"
    context_object_name = "hospitalisations"

    def get_queryset(self):
        return Hospitalisation.objects.filter(deleted_at__isnull=True)  # Hospitalisations non supprimées

# Création d'une hospitalisation
class HospitalisationCreateView(LoginRequiredMixin, SaveByPersonnelMixin, CreateView):
    model = Hospitalisation
    form_class = HospitalisationForm
    template_name = "hospitalisation/hospitalisations/hospitalisation_form.html"
    success_url = reverse_lazy("hospitalisation:hospitalisation_list")


# Détails d'une hospitalisation
class HospitalisationDetailView(DetailView):
    model = Hospitalisation
    template_name = "hospitalisation/hospitalisations/hospitalisation_detail.html"
    context_object_name = "hospitalisation"

    

# Mise à jour d'une hospitalisation
class HospitalisationUpdateView(UpdateView):
    model = Hospitalisation
    form_class = HospitalisationForm
    template_name = "hospitalisation/hospitalisations/hospitalisation_form.html"
    success_url = reverse_lazy("hospitalisation:hospitalisation_list")

# Suppression logique d'une hospitalisation
class HospitalisationDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        hospitalisation = get_object_or_404(Hospitalisation.all_objects, pk=pk)
        hospitalisation.delete()  # Suppression logique
        print(f"Hospitalisation supprimée : {hospitalisation.deleted_at}")  # Vérifie la suppression
        return redirect(reverse_lazy("hospitalisation:hospitalisation_list"))

# Restauration d'une hospitalisation supprimée
class HospitalisationRestoreView(View):
    def post(self, request, pk):
        # Récupérer l'hospitalisation supprimée
        hospitalisation = get_object_or_404(Hospitalisation.all_objects, pk=pk)    
        # Restaurer l'hospitalisation
        hospitalisation.restore()
        # Optionnel: afficher une confirmation dans la console
        print(f"Hospitalisation restaurée : {hospitalisation.id}")
        # Rediriger vers la liste des hospitalisations supprimées
        return redirect(reverse_lazy("hospitalisation:hospitalisation_deleted_list"))


# Liste des hospitalisations supprimée
class HospitalisationDeletedListView(ListView):
    model = Hospitalisation
    template_name = "hospitalisation/hospitalisations/hospitalisation_deleted_list.html"
    context_object_name = "hospitalisations_deleted"  # Correct

    def get_queryset(self):
        return Hospitalisation.all_objects.filter(deleted_at__isnull=False)  # Hospitalisations supprimées


