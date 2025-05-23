from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.utils.timezone import now
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Mto
from .forms import MtoForm
from personnels.mixins import SaveByPersonnelMixin

# Liste des Mtos actifs (non supprimés)
class MtoListView(ListView):
    model = Mto
    template_name = "mto/mtos/mto_list.html"
    context_object_name = "mtos"

    def get_queryset(self):
        return Mto.objects.filter(deleted_at__isnull=True)  # Mtos non supprimés

# Création d'un Mto
class MtoCreateView(LoginRequiredMixin, SaveByPersonnelMixin, CreateView):
    model = Mto
    form_class = MtoForm
    template_name = "mto/mtos/mto_form.html"
    success_url = reverse_lazy("mto:mto_list")


# Détails d'un Mto
class MtoDetailView(DetailView):
    model = Mto
    template_name = "mto/mtos/mto_detail.html"
    context_object_name = "mto"

# Mise à jour d'un Mto
class MtoUpdateView(UpdateView):
    model = Mto
    form_class = MtoForm
    template_name = "mto/mtos/mto_form1.html"
    success_url = reverse_lazy("mto:mto_list")

# Suppression logique d'un Mto
class MtoDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        mto = get_object_or_404(Mto, pk=pk)
        mto.deleted_at = now()  # Marquer comme supprimé
        mto.save()  # Sauvegarder l'objet avec la date de suppression
        print(f"Mto supprimé : {mto.deleted_at}")  # Vérifier la suppression
        return redirect(reverse_lazy("mto:mto_list"))

# Restauration d'un Mto supprimé
class MtoRestoreView(View):
    def post(self, request, pk):
        mto = get_object_or_404(Mto.all_objects, pk=pk)  # Récupérer même les supprimés
        if mto.deleted_at:  # Vérifier qu'il est bien supprimé
            mto.restore()  # Restaurer l’objet
        return redirect(reverse_lazy("mto:mto_deleted_list"))  # Redirection vers la corbeille

# Liste des Mtos supprimés
class MtoDeletedListView(ListView):
    model = Mto
    template_name = "mto/mtos/mto_deleted_list.html"
    context_object_name = "mtos_deleted"

    def get_queryset(self):
        return Mto.all_objects.filter(deleted_at__isnull=False)  #  Récupère les supprimés

