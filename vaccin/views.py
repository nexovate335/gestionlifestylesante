from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.utils.timezone import now
from .models import Vaccin
from .forms import VaccinForm

#  Liste des vaccins actifs
class VaccinListView(ListView):
    model = Vaccin
    template_name = "vaccin/vaccin_list.html"
    context_object_name = "vaccins"

    def get_queryset(self):
        return Vaccin.objects.filter(deleted_at__isnull=True)

#  Création d'un vaccin
class VaccinCreateView(CreateView):
    model = Vaccin
    form_class = VaccinForm
    template_name = "vaccin/vaccin_form.html"
    success_url = reverse_lazy("vaccin:vaccin_list")

#  Détails d'un vaccin
class VaccinDetailView(DetailView):
    model = Vaccin
    template_name = "vaccin/vaccin_detail.html"
    context_object_name = "vaccin"

#  Mise à jour d'un vaccin
class VaccinUpdateView(UpdateView):
    model = Vaccin
    form_class = VaccinForm
    template_name = "vaccin/vaccin_form1.html"
    success_url = reverse_lazy("vaccin:vaccin_list")

#  Suppression logique d'un vaccin
class VaccinDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        vaccin = get_object_or_404(Vaccin, pk=pk)
        vaccin.deleted_at = now()  #  Marquer comme supprimé
        vaccin.save(update_fields=["deleted_at"])  # Optimisation
        return redirect(reverse_lazy("vaccin:vaccin_list"))

#  Restauration d'un vaccin supprimé
class VaccinRestoreView(View):
    def post(self, request, pk):
        vaccin = get_object_or_404(Vaccin.all_objects, pk=pk)  #  On utilise all_objects
        vaccin.deleted_at = None  #  Restaure le vaccin
        vaccin.save(update_fields=["deleted_at"])  # Optimisation
        return redirect(reverse_lazy("vaccin:vaccin_deleted_list"))

#  Liste des vaccins supprimés
class VaccinDeletedListView(ListView):
    model = Vaccin
    template_name = "vaccin/vaccin_deleted_list.html"
    context_object_name = "vaccins_deleted"

    def get_queryset(self):
        queryset = Vaccin.all_objects.filter(deleted_at__isnull=False)  #  Utiliser all_objects
        print(queryset)  # Debug pour voir si la liste des vaccins supprimés s'affiche bien
        return queryset
