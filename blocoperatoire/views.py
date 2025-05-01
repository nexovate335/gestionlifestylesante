from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from .models import BlocOperatoire
from .forms import BlocOperatoireForm, BlocOperatoireUpdateForm

# Liste des blocs opératoires actifs
class BlocOperatoireListView(ListView):
    model = BlocOperatoire
    template_name = "blocoperatoire/blocoperatoires/blocoperatoire_list.html"
    context_object_name = "blocs"

    def get_queryset(self):
        # On récupère uniquement les blocs opératoires non supprimés
        return BlocOperatoire.objects.all()
    
       
class BlocOperatoireRecepListView(ListView):
    model = BlocOperatoire
    template_name = "blocoperatoire/blocoperatoires/blocoperatoire_list_recep.html"
    context_object_name = "blocs"

    def get_queryset(self):
        # On récupère uniquement les blocs opératoires non supprimés
        return BlocOperatoire.objects.all()


# Création d'un bloc opératoire
class BlocOperatoireCreateView(CreateView):
    model = BlocOperatoire
    form_class = BlocOperatoireForm
    template_name = "blocoperatoire/blocoperatoires/blocoperatoire_form.html"
    success_url = reverse_lazy("blocoperatoire:blocoperatoire_list_recep")

    def form_valid(self, form):
        bloc = form.save(commit=False)
        bloc.deleted_at = None  # S'assurer que le champ est bien NULL
        bloc.save()
        return redirect(self.success_url)

# Détails d'un bloc opératoire
class BlocOperatoireDetailView(DetailView):
    model = BlocOperatoire
    template_name = "blocoperatoire/blocoperatoires/blocoperatoire_detail.html"
    context_object_name = "blocoperatoire"

# Mise à jour d'un bloc opératoire
class BlocOperatoireUpdateView(UpdateView):
    model = BlocOperatoire
    form_class = BlocOperatoireForm
    template_name = "blocoperatoire/blocoperatoires/blocoperatoire_form.html"
    success_url = reverse_lazy("blocoperatoire:blocoperatoire_list_recep")
    
    
class BlocOperatoireUserUpdateView(UpdateView):
    model = BlocOperatoire
    form_class = BlocOperatoireUpdateForm
    template_name = "blocoperatoire/blocoperatoires/blocoperatoire_form1.html"
    success_url = reverse_lazy("blocoperatoire:blocoperatoire_list")


# Suppression logique d'un bloc opératoire
class BlocOperatoireDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        # Récupère le bloc opératoire, même s'il est supprimé
        bloc = get_object_or_404(BlocOperatoire.all_objects, pk=pk)
        bloc.delete()  # Appelle la méthode de suppression logique
        return redirect(reverse_lazy("blocoperatoire:blocoperatoire_list"))

# Restauration d'un bloc opératoire supprimé
class BlocOperatoireRestoreView(View):
    def post(self, request, pk):
        bloc = get_object_or_404(BlocOperatoire.all_objects, pk=pk)
        bloc.restore()  # Utiliser la méthode restore() définie dans le modèle
        return redirect(reverse_lazy("blocoperatoire:blocoperatoire_deleted_list"))

# Liste des blocs opératoires supprimés
class BlocOperatoireDeletedListView(ListView):
    model = BlocOperatoire
    template_name = "blocoperatoire/blocoperatoires/blocoperatoire_deleted_list.html"
    context_object_name = "blocs_supprimes"

    def get_queryset(self):
        # On récupère tous les blocs opératoires supprimés
        return BlocOperatoire.all_objects.filter(deleted_at__isnull=False)

