from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from personnels.mixins import SaveByPersonnelMixin
from .models import Pansement
from patients.models import Patient
from .forms import PansementForm
from django.http import JsonResponse



# Vue pour la liste des pansements actifs
class PansementListView(ListView):
    model = Pansement
    template_name = "pansement/pansements/pansement_list.html"
    context_object_name = "pansements"

    def get_queryset(self):
        # Récupère les pansements actifs uniquement
        return Pansement.objects.all().order_by('-date')



# Vue pour la création d'un pansement
class PansementCreateView(LoginRequiredMixin, SaveByPersonnelMixin, CreateView):
    model = Pansement
    form_class = PansementForm
    template_name = "pansement/pansements/pansement_form.html"
    success_url = reverse_lazy("pansement:pansement_list")


# Vue pour les détails d'un pansement
class PansementDetailView(DetailView):
    model = Pansement
    template_name = "pansement/pansements/pansement_detail.html"
    context_object_name = "pansement"

    # Utilisation de la méthode get_object pour récupérer l'objet
    def get_object(self, queryset=None):
        # Cette méthode est automatiquement appelée par DetailView
        return get_object_or_404(Pansement, pk=self.kwargs['pk'])

    # Si vous devez ajouter des données contextuelles supplémentaires, vous pouvez les ajouter ici
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Vous pouvez ajouter d'autres données dans le contexte si nécessaire
        return context


# Vue pour la mise à jour d'un pansement
class PansementUpdateView(UpdateView):
    model = Pansement
    form_class = PansementForm
    template_name = "pansement/pansements/pansement_form1.html"
    success_url = reverse_lazy("pansement:pansement_list")




# Vue pour la suppression d'un pansement (marquer comme supprimé)
class PansementDeleteView(View):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Pansement, pk=kwargs["pk"])
        obj.delete()  # Utilise la méthode `delete()` définie dans le modèle
        return redirect("/pansement/")  # Redirige vers la liste des pansements actifs


# Vue pour restaurer un pansement supprimé
class PansementRestoreView(View):
    def get(self, request, pk):
        # Cherche le pansement dans tous les objets, y compris les supprimés
        pansement = get_object_or_404(Pansement.objects.all(), pk=pk)
        
        # Restaure le pansement
        pansement.restore()
        
        # Redirige vers la liste des pansements supprimés
        return redirect('pansement:pansement_deleted_list')

# Vue pour la liste des pansements supprimés
class PansementDeletedListView(ListView):
    model = Pansement
    template_name = "pansement/pansements/pansement_deleted_list.html"
    context_object_name = "pansements_deleted"

    def get_queryset(self):
        # Récupère les pansements supprimés (où `deleted_at` n'est pas null)
        return Pansement.objects.filter(deleted_at__isnull=False)


def patient_autocomplete_api(request):
    term = request.GET.get("q", "")
    patients = Patient.objects.filter(nom__icontains=term)[:10]

    results = []
    for patient in patients:
        results.append({
            "id": patient.id,
            "text": f"{patient.nom} {patient.prenom}"
        })

    return JsonResponse({"results": results})
