from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView,  View
)
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from patients.models import Patient
from .models import Echographie
from .forms import EchographieForm
from personnels.mixins import SaveByPersonnelMixin

# Liste des échographies
class EchographieListView(ListView):
    model = Echographie
    template_name = "echographie/echographies/echographie_list.html"
    context_object_name = "echographies"

    def get_queryset(self):
        return Echographie.objects.all().order_by('-date') 

# Création d'une échographie
class EchographieCreateView(LoginRequiredMixin, SaveByPersonnelMixin, CreateView):
    model = Echographie
    form_class = EchographieForm
    template_name = "echographie/echographies/echographie_form.html"
    success_url = reverse_lazy("echographie:echographie_list")
    


# Détails d'une échographie
class EchographieDetailView(DetailView):
    model = Echographie
    template_name = "echographie/echographies/echographie_detail.html"
    context_object_name = "echographie"
    

# Mise à jour d'une échographie
class EchographieUpdateView(UpdateView):
    model = Echographie
    form_class = EchographieForm
    template_name = "echographie/echographies/echographie_form1.html"
    success_url = reverse_lazy("echographie:echographie_list")
    
    

# Suppression logique d'une échographie
class EchographieDeleteView(View):
    def post(self, request, *args, **kwargs):
        echographie = get_object_or_404(Echographie.objects, pk=self.kwargs["pk"])  
        echographie.deleted_at = now()
        echographie.save()
        return redirect(reverse_lazy("echographie:echographie_list"))

    
# Restauration d'une échographie supprimée
class EchographieRestoreView(View):
    def post(self, request, pk):
        echographie = get_object_or_404(Echographie.all_objects.filter(deleted_at__isnull=False), pk=pk)    
        echographie.restore()
        return redirect(reverse_lazy("echographie:echographie_deleted_list"))

# Liste des echographie supprimés
class EchographieDeletedListView(ListView):
    model = Echographie
    template_name = "echographie/echographies/echographie_deleted_list.html"
    context_object_name = "echographies_deleted"

    def get_queryset(self):
        return Echographie.all_objects.filter(deleted_at__isnull=False)


