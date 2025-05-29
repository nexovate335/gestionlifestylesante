from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now
from datetime import datetime
from django.utils.timezone import localtime
from .models import FactureCaisse, Caisse, AutresDepenses, RapportJournalierCaisse
from .forms import FactureCaisseForm, FactureCaisseFormUpdate, CaisseFormSet, AutresDepensesForm, RapportJournalierCaisseForm

#  Liste des factures (remplace `liste_factures_caisse`)
@method_decorator(login_required, name='dispatch')
class FactureCaisseRecepListView(ListView):
    model = FactureCaisse
    template_name = "caisse/factures/facture_list_caisse_recep.html"
    context_object_name = "factures"

    def get_queryset(self):
        queryset = FactureCaisse.objects.all().order_by("-facture_date_time")

        date = self.request.GET.get("date")
        date_debut = self.request.GET.get("date_debut")
        date_fin = self.request.GET.get("date_fin")

        if date:
            queryset = queryset.filter(facture_date_time__date=date)
        elif date_debut and date_fin:
            queryset = queryset.filter(facture_date_time__date__range=[date_debut, date_fin])
        elif date_debut:
            queryset = queryset.filter(facture_date_time__date__gte=date_debut)
        elif date_fin:
            queryset = queryset.filter(facture_date_time__date__lte=date_fin)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["date"] = self.request.GET.get("date", "")
        context["date_debut"] = self.request.GET.get("date_debut", "")
        context["date_fin"] = self.request.GET.get("date_fin", "")
        return context
    
        
@method_decorator(login_required, name='dispatch')
class FactureCaisseListView(ListView):
    model = FactureCaisse
    template_name = "caisse/factures/facture_list_caisse.html"
    context_object_name = "factures"

    def get_queryset(self):
        queryset = FactureCaisse.objects.all().order_by("-facture_date_time")
        date_str = self.request.GET.get("date")
        date_debut = self.request.GET.get("date_debut")
        date_fin = self.request.GET.get("date_fin")

        # Filtrage par date exacte (prioritaire)
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
                queryset = queryset.filter(facture_date_time__date=date_obj)
            except ValueError:
                pass  # date invalide

        # Sinon, filtrage par plage de dates
        elif date_debut or date_fin:
            try:
                if date_debut:
                    date_debut_obj = datetime.strptime(date_debut, "%Y-%m-%d").date()
                    queryset = queryset.filter(facture_date_time__date__gte=date_debut_obj)
                if date_fin:
                    date_fin_obj = datetime.strptime(date_fin, "%Y-%m-%d").date()
                    queryset = queryset.filter(facture_date_time__date__lte=date_fin_obj)
            except ValueError:
                pass  # Ignore les dates invalides

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localtime().date()
        context["factures_du_jour"] = FactureCaisse.objects.filter(facture_date_time__date=today).order_by("-facture_date_time")

        # Pour pré-remplir le formulaire dans le template
        context["date"] = self.request.GET.get("date", "")
        context["date_debut"] = self.request.GET.get("date_debut", "")
        context["date_fin"] = self.request.GET.get("date_fin", "")
        return context


#  Création d'une facture (remplace `creer_facturecaisse`)
@method_decorator(login_required, name='dispatch')
class FactureCaisseCreateView(CreateView):
    model = FactureCaisse
    form_class = FactureCaisseForm
    template_name = "caisse/factures/creer_facture_caisse.html"

    def form_valid(self, form):
        facture = form.save(commit=False)
        facture.save_by = self.request.user.personnel
        facture.save()

        self.object = facture  # Important : pour que get_success_url() ait accès à self.object

        formset = CaisseFormSet(self.request.POST)
        if formset.is_valid():
            caisses = formset.save(commit=False)
            for caisse in caisses:
                caisse.facture = facture
                caisse.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('caisse:modifier_facture_caisse', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = CaisseFormSet()
        return context
#  Modification d'une facture (remplace `modifier_factureCaisse`)
@method_decorator(login_required, name='dispatch')
class FactureCaisseUpdateView(UpdateView):
    model = FactureCaisse
    form_class = FactureCaisseFormUpdate
    template_name = "caisse/factures/facturecaisse_update.html"

    def get_success_url(self):
        return reverse("caisse:voir_facture_caisse", args=[self.object.numero_facture])

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

#  Détail d'une facture (remplace `voir_facturecaisse`)
@method_decorator(login_required, name='dispatch')
class FactureCaisseDetailView(DetailView):
    model = FactureCaisse
    template_name = "caisse/factures/voir_facturecaisse.html"
    context_object_name = "facture"

    def get_object(self):
        """ Récupère la facture par son numéro de facture """
        numero_facture = self.kwargs.get("numero_facture")
        return get_object_or_404(FactureCaisse, numero_facture=numero_facture)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["caisses"] = Caisse.objects.filter(facture=self.object)
        return context


# Lister toutes les dépenses (sauf celles supprimées)
@method_decorator(login_required, name='dispatch')
class AutresDepensesListView(ListView):
    model = AutresDepenses
    template_name = "caisse/autres_depenses_list.html"
    context_object_name = "depenses"

    def get_queryset(self):
        return AutresDepenses.objects.filter(deleted_at__isnull=True).order_by('-date')


# Ajouter une dépense
@method_decorator(login_required, name='dispatch')
class AutresDepensesCreateView(CreateView):
    model = AutresDepenses
    form_class = AutresDepensesForm
    template_name = "caisse/autres_depenses_form.html"
    success_url = reverse_lazy("caisse:autres_depenses_list")

   
# Modifier une dépense
@method_decorator(login_required, name='dispatch')
class AutresDepensesUpdateView(UpdateView):
    model = AutresDepenses
    form_class = AutresDepensesForm
    template_name = "pharmacie/autres_depenses_form.html"
    success_url = reverse_lazy("caisse:autres_depenses_list")


#  Supprimer (soft delete) une dépense
@method_decorator(login_required, name='dispatch')
class AutresDepensesDeleteView(DeleteView):
    model = AutresDepenses
    template_name = "pharmacie/autres_depenses_confirm_delete.html"
    success_url = reverse_lazy("caisse:autres_depenses_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return self.redirect(self.success_url)


@method_decorator(login_required, name='dispatch')
class RapportJournalierCaisseListView(ListView):
    model = RapportJournalierCaisse
    template_name = "caisse/rapport_journalier_list.html"
    context_object_name = "rapports"

    def get_queryset(self):
        return RapportJournalierCaisse.objects.filter(deleted_at__isnull=True).order_by('-date')



@method_decorator(login_required, name='dispatch')
class RapportJournalierCaisseCreateView(CreateView):
    model = RapportJournalierCaisse
    form_class = RapportJournalierCaisseForm
    template_name = "caisse/rapport_journalier_form.html"
    success_url = reverse_lazy("caisse:rapport_journalier_list")

    def form_valid(self, form):
        rapport = form.save(commit=False)
        #on peut récupérer le caissier via l'utilisateur connecté
        rapport.caissier = str(self.request.user.personnel.user)
        rapport.save()
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class RapportJournalierCaisseUpdateView(UpdateView):
    model = RapportJournalierCaisse
    fields = ['caissier', 'total_encaisse', 'depense']
    template_name = "caisse/rapport_journalier_form.html"
    success_url = reverse_lazy("caisse:rapport_journalier_list")

    def get_queryset(self):
        return RapportJournalierCaisse.objects.filter(deleted_at__isnull=True)


@method_decorator(login_required, name='dispatch')
class RapportJournalierCaisseDeleteView(DeleteView):
    model = RapportJournalierCaisse
    template_name = "caisse/rapport_journalier_confirm_delete.html"
    success_url = reverse_lazy("caisse:rapport_journalier_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()  # Appelle la méthode `delete()` du modèle (soft delete)
        return self.redirect(self.success_url)

    def get_queryset(self):
        return RapportJournalierCaisse.objects.filter(deleted_at__isnull=True)
