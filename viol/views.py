from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.utils.timezone import now
from .models import Viol
from .forms import ViolForm

#  Liste des Viols actifs
class ViolListView(ListView):
    model = Viol
    template_name = "viol/viol_list.html"
    context_object_name = "viols"

    def get_queryset(self):
        return Viol.objects.filter(deleted_at__isnull=True)

#  Création d'un Viol
class ViolCreateView(CreateView):
    model = Viol
    form_class = ViolForm
    template_name = "viol/viol_form.html"
    success_url = reverse_lazy("viol:viol_list")

#  Détails d'un Viol
class ViolDetailView(DetailView):
    model = Viol
    template_name = "viol/viol_detail.html"
    context_object_name = "viol"

#  Mise à jour d'un Viol
class ViolUpdateView(UpdateView):
    model = Viol
    form_class = ViolForm
    template_name = "viol/viol_form1.html"
    success_url = reverse_lazy("viol:viol_list")

#  Suppression logique
class ViolDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        viol = get_object_or_404(Viol, pk=pk)
        viol.delete()
        return redirect(reverse_lazy("viol:viol_list"))

#  Restauration d'un Viol supprimé
class ViolRestoreView(View):
    def post(self, request, pk):
        viol = get_object_or_404(Viol.all_objects.all(), pk=pk)  #  Correction ajout .all()
        viol.restore()
        return redirect(reverse_lazy("viol:viol_deleted_list"))

#  Liste des Viols supprimés
class ViolDeletedListView(ListView):
    model = Viol
    template_name = "viol/viol_deleted_list.html"
    context_object_name = "viols_deleted"

    def get_queryset(self):
        return Viol.all_objects.all().filter(deleted_at__isnull=False)  #  Correction ajout .all()
