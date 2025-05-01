from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from .models import RendezVous
from .forms import RendezVousForm

# Liste des rendez-vous actifs
class RendezVousListView(ListView):
    model = RendezVous
    template_name = "rendez_vous/rendezvous_liste.html"
    context_object_name = "rendezvous"

    def get_queryset(self):
        return RendezVous.objects.all()  # Affiche les rendez-vous actifs

# Création d'un rendez-vous
class RendezVousCreateView(CreateView):
    model = RendezVous
    form_class = RendezVousForm
    template_name = "rendez_vous/rendezvous_form.html"
    success_url = reverse_lazy("rendezvous:rendezvous_list")

# Détails d'un rendez-vous
class RendezVousDetailView(DetailView):
    model = RendezVous
    template_name = "rendez_vous/rendezvous_detail.html"
    context_object_name = "rendez_vous"

# Mise à jour d'un rendez-vous
class RendezVousUpdateView(UpdateView):
    model = RendezVous
    form_class = RendezVousForm
    template_name = "rendez_vous/rendezvous_form1.html"
    success_url = reverse_lazy("rendezvous:rendezvous_list")

# Suppression logique d'un rendez-vous
class RendezVousDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        rendez_vous = get_object_or_404(RendezVous, pk=pk)
        rendez_vous.delete()  # Cette suppression marque le rendez-vous comme supprimé
        return redirect(reverse_lazy("rendezvous:rendezvous_list"))


# Restauration d'un rendez-vous supprimé
class RendezVousRestoreView(View):
    def get(self, request, pk):
        rendez_vous = get_object_or_404(RendezVous.all_objects, pk=pk)  # Récupère même les supprimés
        rendez_vous.restore()  # Restaure le RendezVous
        return render(request, 'rendez_vous/rendezvous_deleted_list.html', {'rendez_vous': rendez_vous})
        

# Liste des rendez-vous supprimés
class RendezVousDeletedListView(ListView):
    model = RendezVous
    template_name = "rendez_vous/rendezvous_deleted_list.html"
    context_object_name = "deleted_rendezvous"

    def get_queryset(self):
        return RendezVous.deleted_objects.all()  # Récupérer les objets supprimés

