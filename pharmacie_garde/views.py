from django.utils import timezone
from django.utils.timezone import now
from django.utils.timezone import localtime
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect,render
from django.utils.decorators import method_decorator
from django.urls import reverse 
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import  PhGardeCommande, PhGardeStock, PhGardeFacturePharmacie, PhGardeFactureAvance, PhGardeVente
from .forms import *



# --- CRUD POUR PRODUIT ---
# Liste des produits actifs
class PhGardeProduitListView(ListView):
    model = PhGardeProduit
    template_name = "pharmacie_garde/phgardeproduits/phgardeproduit_list.html"
    context_object_name = "produits"

    def get_queryset(self):
        return PhGardeProduit.objects.filter(deleted_at__isnull=True)  # Produits non supprimés

# Création d'un produit
class PhGardeProduitCreateView(CreateView):
    model = PhGardeProduit
    form_class = PhGardeProduitForm
    template_name = "pharmacie_garde/phgardeproduits/phgardeproduit_form.html"
    success_url = reverse_lazy("pharmacie_garde:phgardeproduit_list")

# Détails d'un produit
class PhGardeProduitDetailView(DetailView):
    model = PhGardeProduit
    template_name = "pharmacie_garde/phgardeproduits/phgardeproduit_detail.html"
    context_object_name = "produit"

# Mise à jour d'un produit
class PhGardeProduitUpdateView(UpdateView):
    model = PhGardeProduit
    form_class = PhGardeProduitForm
    template_name = "pharmacie_garde/phgardeproduits/phgardeproduit_form1.html"
    success_url = reverse_lazy("pharmacie_garde:phgardeproduit_list")

class PhGardeProduitDeleteView(View):
    def get(self, request, pk):
        produit = get_object_or_404(PhGardeProduit, pk=pk)
        return render(request, 'pharmacie_garde/phgardeproduit_delete.html', {'produit': produit})

    def post(self, request, pk):
        produit = get_object_or_404(PhGardeProduit, pk=pk)
        produit.delete()
        return redirect('pharmacie_garde:phgardeproduit_list')

# Restauration d'un produit supprimé
class PhGardeProduitRestoreView(View):
    def get(self, request, pk):
        produit = get_object_or_404(PhGardeProduit.all_objects, pk=pk)  # Récupère même les supprimés
        produit.restore()  # Restaure le produit
        return redirect(reverse_lazy("pharmacie_garde:phgardeproduit_deleted_list"))

# Liste des produits supprimés
class PhGardeProduitDeletedListView(ListView):
    model = PhGardeProduit
    template_name = 'pharmacie_garde/phgardeproduits/phgardeproduit_deleted_list.html'
    context_object_name = 'produits_deleted'

    def get_queryset(self):
        # Utiliser le manager pour obtenir les produits supprimés
        return PhGardeProduit.objects.deleted()  # Utiliser la méthode deleted() pour filtrer


# --- CRUD POUR COMMANDE ---
# Liste des commandes actives
class PhGardeCommandeListView(ListView):
    model = PhGardeCommande
    template_name = "pharmacie_garde/phgardecommandes/phgardecommande_list.html"
    context_object_name = "commandes"

    def get_queryset(self):
        return PhGardeCommande.objects.filter(deleted_at__isnull=True).order_by('produit__nom_produit')

# Création d'une commande
class PhGardeCommandeCreateView(CreateView):
    model = PhGardeCommande
    form_class = PhGardeCommandeForm
    template_name = "pharmacie_garde/phgardecommandes/phgardecommande_form.html"
    success_url = reverse_lazy("pharmacie_garde:phgardecommande_list")

# Détails d'une commande
class PhGardeCommandeDetailView(DetailView):
    model = PhGardeCommande
    template_name = "pharmacie_garde/phgardecommandes/phgardecommande_detail.html"
    context_object_name = "commande"

# Mise à jour d'une commande
class PhGardeCommandeUpdateView(UpdateView):
    model = PhGardeCommande
    form_class = PhGardeCommandeForm
    template_name = "pharmacie_garde/phgardecommandes/phgardecommande_form.html"
    success_url = reverse_lazy("pharmacie_garde:phgardecommande_list")

# Suppression logique d'une commande
class PhGardeCommandeDeleteView(View):
    def get(self, request, pk):
        commande = get_object_or_404(PhGardeCommande, pk=pk)
        return render(request, "pharmacie_garde/phgardecommandes/phgardecommande_confirm_delete.html", {"commande": commande})

    def post(self, request, pk):
        commande = get_object_or_404(PhGardeCommande, pk=pk)
        commande.delete()  # Suppression logique
        return redirect("Pharmacie_garde:phgardecommande_list")

# Restauration d'une commande supprimée
class PhGardeCommandeRestoreView(View):
    def get(self, request, pk):
        commande = get_object_or_404(PhGardeCommande.all_objects, pk=pk)  # Récupérer même les commandes supprimées
        commande.restore()  # Restaurer la commande
        return redirect("pharmacie_garde:phgardecommande_deleted_list")

# Liste des commandes supprimées
class PhGardeCommandeDeletedListView(ListView):
    model = PhGardeCommande
    template_name = "pharmacie_garde/phgardecommandes/phgardecommande_deleted_list.html"
    context_object_name = "commandes_deleted"

    def get_queryset(self):
        return PhGardeCommande.objects.deleted()  # Utiliser le manager personnalisé pour récupérer les commandes supprimées


# --- CRUD POUR STOCK ---

class PhGardeGestionStockListView(ListView):
    model = PhGardeStock
    template_name = "pharmacie_garde/phgardestocks/phgardegestion_stock_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        return PhGardeStock.objects.filter(deleted_at__isnull=True).order_by('produit__nom_produit')  # Produits non supprimés
    
    
class PhGardeStockListView(ListView):
    model = PhGardeStock
    template_name = "pharmacie_garde/phgardestocks/phgardestock_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        return PhGardeStock.objects.filter(deleted_at__isnull=True).order_by('produit__nom_produit')  # Produits non supprimés


class PhGardeStockCreateView(CreateView):
    model = PhGardeStock
    form_class = PhGardeStockForm
    template_name = "pharmacie_garde/phgardestocks/phgardestock_form.html"
    success_url = reverse_lazy('pharmacie_garde:phgardestock_list')

    def form_valid(self, form):
        produit = form.cleaned_data['produit']
        
        # Vérifier si un Stock existe déjà pour ce produit
        if PhGardeStock.objects.filter(produit=produit).exists():
            form.add_error('produit', 'Ce produit a déjà un stock associé.')
            return self.form_invalid(form)

        return super().form_valid(form)


class PhGardeStockDetailView(DetailView):
    model = PhGardeStock
    template_name = "pharmacie_garde/phgardestocks/phgardestock_detail.html"
    context_object_name = "stock"

class PhGardeStockUpdateView(UpdateView):
    model = PhGardeStock
    form_class = PhGardeStockForm
    template_name = "pharmacie_garde/phgardestocks/phgardestock_form1.html"
    success_url = reverse_lazy('pharmacie_garde:phgardegestion_stock_list')  # Correction ici

class PhGardeStockDeleteView(DeleteView):
    model = PhGardeStock
    template_name = "pharmacie_garde/phgardestocks/phgardestock_confirm_delete.html"
    success_url = reverse_lazy('pharmacie_garde:phgardegestion_stock_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted_at = timezone.now()  # Marquer comme supprimé
        obj.save()
        return redirect(self.success_url)

class PhGardeStockRestoreView(View):
    def get(self, request, pk):
        # Récupère le stock, y compris ceux supprimés logiquement
        stock = get_object_or_404(PhGardeStock.all_objects, pk=pk)  # Utilise all_objects pour inclure les objets supprimés
        stock.restore()  # Restaure le stock
        return redirect('pharmacie_garde:phgardegestion_stock_list')

class PhGardeStockDeletedListView(ListView):
    model = PhGardeStock
    template_name = "pharmacie_garde/phgardestocks/phgardestock_deleted_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        # Utilise 'deleted_at' pour filtrer les stocks supprimés
        return PhGardeStock.objects.deleted()


#  Liste des factures (remplace `liste_factures_pharmacie`)
@method_decorator(login_required, name='dispatch')
class PhGardeFacturePharmacieListView(ListView):
    model = PhGardeFacturePharmacie
    template_name = "pharmacie_garde/phgardefactures/phgardefacture_list_pharmacie.html"
    context_object_name = "factures"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localtime().date()
        context["factures_du_jour"] = PhGardeFacturePharmacie.objects.filter(facture_date_time__date=today)
        return context
    
@method_decorator(login_required, name='dispatch')
class PhGardeFacturePharmacieCaisseListView(ListView):
    model = PhGardeFacturePharmacie
    template_name = "pharmacie_garde/phgardefactures/phgardecaisse_facture_list_pharmacie.html"
    context_object_name = "factures"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localtime().date()
        context["factures_du_jour"] = PhGardeFacturePharmacie.objects.filter(facture_date_time__date=today)
        return context


@method_decorator(login_required, name='dispatch')
class PhGardeFacturePharmacieRecepListView(ListView):
    model = PhGardeFacturePharmacie
    template_name = "pharmacie_garde/phgardefactures/phgarderecep_facture_list_pharmacie.html"
    context_object_name = "factures"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = localtime().date()
        context["factures_du_jour"] = PhGardeFacturePharmacie.objects.filter(facture_date_time__date=today)
        return context
    

# Création d'une facture (remplace `creer_facturepharmacie`)
@method_decorator(login_required, name='dispatch')
class PhGardeFacturePharmacieCreateView(CreateView):
    model = PhGardeFacturePharmacie
    form_class = PhGardeFacturePharmacieForm
    template_name = "pharmacie_garde/phgardefactures/phgardecreer_facturepharmacie.html"
    success_url = reverse_lazy("pharmacie_garde:liste_factures_phgarde")

    def form_valid(self, form):
        facture = form.save(commit=False)
        facture.save_by = self.request.user.personnel  # Associe l'utilisateur connecté
        facture.save()

        formset = PhGardeVenteFormSet(self.request.POST)
        if formset.is_valid():
            ventes = formset.save(commit=False)
            for vente in ventes:
                vente.facture = facture
                vente.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = PhGardeVenteFormSet()
        return context

#  Modification d'une facture (remplace `modifier_facturePharmacie`)
@method_decorator(login_required, name='dispatch')
class PhGardeFacturePharmacieUpdateView(UpdateView):
    model = PhGardeFacturePharmacie
    form_class = PhGardeFacturePharmacieFormUpdate
    template_name = "pharmacie_garde/phgardefactures/phgardefacturepharmacie_update.html"
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
    
    def get_success_url(self):
            return reverse('pharmacie_garde:voir_facture_phgarde', args=[self.object.numero_facture])

#  Détail d'une facture (remplace `voir_facture_pharmacie`)
@method_decorator(login_required, name='dispatch')
class PhGardeFacturePharmacieDetailView(DetailView):
    model = PhGardeFacturePharmacie
    template_name = "pharmacie_garde/phgardefactures/phgardevoir_facturepharmacie.html"
    context_object_name = "facture"

    def get_object(self):
        """ Récupère la facture par son numéro de facture """
        numero_facture = self.kwargs.get("numero_facture")
        return get_object_or_404(PhGardeFacturePharmacie, numero_facture=numero_facture)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ventes"] = PhGardeVente.objects.filter(facture=self.object)
        return context