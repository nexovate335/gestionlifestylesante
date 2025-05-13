from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.urls import reverse
from django.utils.timezone import localtime
from .models import FactureCaisseGarde, CaisseGarde, AutresDepensesGarde, RapportJournalierCaisseGarde
from .forms import FactureCaisseGardeForm, FactureCaisseGardeFormUpdate, CaisseFormSet, AutresDepensesGardeForm, RapportJournalierCaisseGardeForm

#  Liste des factures (remplace `liste_factures_caisse`)
@method_decorator(login_required, name='dispatch')
class FactureCaisseRecepGardeListView(ListView):
    model = FactureCaisseGarde
    template_name = "caisse_garde/factures_garde/facture_list_caisse_recep_garde.html"
    context_object_name = "factures"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localtime().date()
        context["factures_du_jour"] = FactureCaisseGarde.objects.filter(facture_date_time__date=today)
        return context
    
@method_decorator(login_required, name='dispatch')
class FactureCaisseGardeListView(ListView):
    model = FactureCaisseGarde
    template_name = "caisse_garde/factures_garde/facture_list_caisse_garde.html"
    context_object_name = "factures"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localtime().date()
        context["factures_du_jour"] = FactureCaisseGarde.objects.filter(facture_date_time__date=today)
        return context

#  Création d'une facture (remplace `creer_facturecaisse`)
@method_decorator(login_required, name='dispatch')
class FactureCaisseGardeCreateView(CreateView):
    model = FactureCaisseGarde
    form_class = FactureCaisseGardeForm
    template_name = "caisse_garde/factures_garde/creer_facture_caisse_garde.html"
    
    def form_valid(self, form):
        facture = form.save(commit=False)
        facture.save_by = self.request.user.personnel  # Associe l'utilisateur connecté
        facture.save()

        formset = CaisseFormSet(self.request.POST)
        if formset.is_valid():
            caisses = formset.save(commit=False)
            for caisse in caisses:
                caisse.facture = facture
                caisse.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('caisse_garde:modifier_facture_caisse_garde', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = CaisseFormSet()
        return context

#  Modification d'une facture (remplace `modifier_factureCaisse`)
@method_decorator(login_required, name='dispatch')
class FactureCaisseGardeUpdateView(UpdateView):
    model = FactureCaisseGarde
    form_class = FactureCaisseGardeFormUpdate
    template_name = "caisse_garde/factures_garde/facturecaisse_update_garde.html"

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('caisse_garde:voir_facture_caisse_garde', args=[self.object.numero_facture])

#  Détail d'une facture (remplace `voir_facturecaisse`)
@method_decorator(login_required, name='dispatch')
class FactureCaisseGardeDetailView(DetailView):
    model = FactureCaisseGarde
    template_name = "caisse_garde/factures_garde/voir_facturecaisse_garde.html"
    context_object_name = "facture"

    def get_object(self):
        """ Récupère la facture par son numéro de facture """
        numero_facture = self.kwargs.get("numero_facture")
        return get_object_or_404(FactureCaisseGarde, numero_facture=numero_facture)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["caisses"] = CaisseGarde.objects.filter(facture=self.object)
        return context


# Lister toutes les dépenses (sauf celles supprimées)
@method_decorator(login_required, name='dispatch')
class AutresDepensesGardeListView(ListView):
    model = AutresDepensesGarde
    template_name = "caisse_garde/autres_depenses_list_garde.html"
    context_object_name = "depenses"

    def get_queryset(self):
        return AutresDepensesGarde.objects.all()


# Ajouter une dépense
@method_decorator(login_required, name='dispatch')
class AutresDepensesGardeCreateView(CreateView):
    model = AutresDepensesGarde
    form_class = AutresDepensesGardeForm
    template_name = "caisse_garde/autres_depenses_form_garde.html"
    success_url = reverse_lazy("caisse_garde:autres_depenses_list_garde")

   
# Modifier une dépense
@method_decorator(login_required, name='dispatch')
class AutresDepensesGardeUpdateView(UpdateView):
    model = AutresDepensesGarde
    form_class = AutresDepensesGardeForm
    template_name = "caisse_garde/autres_depenses_form_garde.html"
    success_url = reverse_lazy("caisse_garde:autres_depenses_list_garde")


#  Supprimer (soft delete) une dépense
@method_decorator(login_required, name='dispatch')
class AutresDepensesGardeDeleteView(DeleteView):
    model = AutresDepensesGarde
    template_name = "caisse_garde/autres_depenses_confirm_delete.html"
    success_url = reverse_lazy("caisse_garde:autres_depenses_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class RapportJournalierCaisseGardeListView(ListView):
    model = RapportJournalierCaisseGarde
    template_name = "caisse_garde/rapport_journalier_list_garde.html"
    context_object_name = "rapports"

    def get_queryset(self):
        return RapportJournalierCaisseGarde.objects.filter(deleted_at__isnull=True)


@method_decorator(login_required, name='dispatch')
class RapportJournalierCaisseGardeCreateView(CreateView):
    model = RapportJournalierCaisseGarde
    form_class = RapportJournalierCaisseGardeForm
    template_name = "caisse_garde/rapport_journalier_form_garde.html"
    success_url = reverse_lazy("caisse_garde:rapport_journalier_list_garde")

    def form_valid(self, form):
        rapport = form.save(commit=False)
        #on peut récupérer le caissier via l'utilisateur connecté
        rapport.caissier = str(self.request.user.personnel.user)
        rapport.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class RapportJournalierCaisseGardeUpdateView(UpdateView):
    model = RapportJournalierCaisseGarde
    fields = ['caissier', 'total_encaisse', 'depense']
    template_name = "caisse_garde/rapport_journalier_form_garde.html"
    success_url = reverse_lazy("caisse:rapport_journalier_list_garde")

    def get_queryset(self):
        return RapportJournalierCaisseGarde.objects.filter(deleted_at__isnull=True)


@method_decorator(login_required, name='dispatch')
class RapportJournalierCaisseGardeDeleteView(DeleteView):
    model = RapportJournalierCaisseGarde
    template_name = "caisse_garde/rapport_journalier_confirm_delete.html"
    success_url = reverse_lazy("caisse_garde:rapport_journalier_list_garde")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Appelle la méthode `delete()` du modèle (soft delete)
        return self.redirect(self.success_url)

    def get_queryset(self):
        return RapportJournalierCaisseGarde.objects.filter(deleted_at__isnull=True)
