from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.utils.timezone import now
from .models import Pansement, Patient
from .forms import PansementForm

# Vue pour la liste des pansements actifs
class PansementListView(ListView):
    model = Pansement
    template_name = "pansement/pansements/pansement_list.html"
    context_object_name = "pansements"

    def get_queryset(self):
        # Récupère les pansements actifs uniquement
        return Pansement.objects.all()



# Vue pour la création d'un pansement
class PansementCreateView(CreateView):
    model = Pansement
    form_class = PansementForm
    template_name = "pansement/pansements/pansement_form.html"
    success_url = "/pansement/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["patients"] = Patient.objects.all()
        return context

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
    template_name = "pansement/pansements/pansement_form.html"
    success_url = "/pansement/"

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
