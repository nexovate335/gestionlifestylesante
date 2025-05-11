from django.utils import timezone
from django.utils.timezone import now
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.shortcuts import get_object_or_404, redirect,render
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Produit, Fournisseur, Commande, Stock, FacturePharmacie, FactureAvance, Vente
from .forms import *


# --- CRUD POUR PRODUIT ---
# Liste des produits actifs
class ProduitListView(ListView):
    model = Produit
    template_name = "pharmacie/produits/produit_list.html"
    context_object_name = "produits"

    def get_queryset(self):
        return Produit.objects.filter(deleted_at__isnull=True)  # Produits non supprimés

# Création d'un produit
class ProduitCreateView(CreateView):
    model = Produit
    form_class = ProduitForm
    template_name = "pharmacie/produits/produit_form.html"
    success_url = reverse_lazy("pharmacie:produit_list")

# Détails d'un produit
class ProduitDetailView(DetailView):
    model = Produit
    template_name = "pharmacie/produits/produit_detail.html"
    context_object_name = "produit"

# Mise à jour d'un produit
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class = ProduitForm
    template_name = "pharmacie/produits/produit_form1.html"
    success_url = reverse_lazy("pharmacie:produit_list")

class ProduitDeleteView(View):
    def get(self, request, pk):
        produit = get_object_or_404(Produit, pk=pk)
        return render(request, 'pharmacie/produit_delete.html', {'produit': produit})

    def post(self, request, pk):
        produit = get_object_or_404(Produit, pk=pk)
        produit.delete()
        return redirect('pharmacie:produit_list')

# Restauration d'un produit supprimé
class ProduitRestoreView(View):
    def get(self, request, pk):
        produit = get_object_or_404(Produit.all_objects, pk=pk)  # Récupère même les supprimés
        produit.restore()  # Restaure le produit
        return redirect(reverse_lazy("pharmacie:produit_deleted_list"))

# Liste des produits supprimés
class ProduitDeletedListView(ListView):
    model = Produit
    template_name = 'pharmacie/produits/produit_deleted_list.html'
    context_object_name = 'produits_deleted'

    def get_queryset(self):
        # Utiliser le manager pour obtenir les produits supprimés
        return Produit.objects.deleted()  # Utiliser la méthode deleted() pour filtrer
        
# --- CRUD POUR FOURNISSEUR ---
# Liste des fournisseurs actifs
class FournisseurListView(ListView):
    model = Fournisseur
    template_name = "pharmacie/fournisseurs/fournisseur_list.html"
    context_object_name = "fournisseurs"
    
    def get_queryset(self):
        return Fournisseur.objects.filter(deleted_at__isnull=True)  # Fournisseurs non supprimés

# Création d'un fournisseur
class FournisseurCreateView(CreateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = "pharmacie/fournisseurs/fournisseur_form.html"
    success_url = reverse_lazy('pharmacie:fournisseur_list')

# Détails d'un fournisseur
class FournisseurDetailView(DetailView):
    model = Fournisseur
    template_name = "pharmacie/fournisseurs/fournisseur_detail.html"
    context_object_name = "fournisseur"

# Mise à jour d'un fournisseur
class FournisseurUpdateView(UpdateView):
    model = Fournisseur
    form_class = FournisseurForm
    template_name = "pharmacie/fournisseurs/fournisseur_form1.html"
    success_url = reverse_lazy('pharmacie:fournisseur_list')

# Suppression logique d'un fournisseur
class FournisseurDeleteView(View):
    def get(self, request, pk):
        fournisseur = get_object_or_404(Fournisseur, pk=pk)
        return render(request, 'pharmacie/fournisseurs/fournisseur_confirm_delete.html', {'fournisseur': fournisseur})

    def post(self, request, pk):
        fournisseur = get_object_or_404(Fournisseur, pk=pk)
        fournisseur.delete()  # Suppression logique
        return redirect('pharmacie:fournisseur_list')

# Restauration d'un fournisseur supprimé
class FournisseurRestoreView(View):
    def get(self, request, pk):
        # Utiliser 'all_objects' pour récupérer même les fournisseurs supprimés
        fournisseur = get_object_or_404(Fournisseur.all_objects, pk=pk)

        # Restaurer le fournisseur
        fournisseur.restore()

        return redirect('pharmacie:fournisseur_list')


# Liste des fournisseurs supprimés
class FournisseurDeletedListView(ListView):
    model = Fournisseur
    template_name = 'pharmacie/fournisseurs/fournisseur_deleted_list.html'
    context_object_name = 'fournisseurs_deleted'
    
    def get_queryset(self):
        return Fournisseur.all_objects.filter(deleted_at__isnull=False)  # Fournisseurs supprimés


# --- CRUD POUR COMMANDE ---
# Liste des commandes actives
class CommandeListView(ListView):
    model = Commande
    template_name = "pharmacie/commandes/commande_list.html"
    context_object_name = "commandes"

    def get_queryset(self):
        return Commande.objects.filter(deleted_at__isnull=True)

# Création d'une commande
class CommandeCreateView(CreateView):
    model = Commande
    form_class = CommandeForm
    template_name = "pharmacie/commandes/commande_form.html"
    success_url = reverse_lazy("pharmacie:commande_list")

# Détails d'une commande
class CommandeDetailView(DetailView):
    model = Commande
    template_name = "pharmacie/commandes/commande_detail.html"
    context_object_name = "commande"

# Mise à jour d'une commande
class CommandeUpdateView(UpdateView):
    model = Commande
    form_class = CommandeForm
    template_name = "pharmacie/commandes/commande_form.html"
    success_url = reverse_lazy("pharmacie:commande_list")

# Suppression logique d'une commande
class CommandeDeleteView(View):
    def get(self, request, pk):
        commande = get_object_or_404(Commande, pk=pk)
        return render(request, "pharmacie/commandes/commande_confirm_delete.html", {"commande": commande})

    def post(self, request, pk):
        commande = get_object_or_404(Commande, pk=pk)
        commande.delete()  # Suppression logique
        return redirect("pharmacie:commande_list")

# Restauration d'une commande supprimée
class CommandeRestoreView(View):
    def get(self, request, pk):
        commande = get_object_or_404(Commande.all_objects, pk=pk)  # Récupérer même les commandes supprimées
        commande.restore()  # Restaurer la commande
        return redirect("pharmacie:commande_deleted_list")

# Liste des commandes supprimées
class CommandeDeletedListView(ListView):
    model = Commande
    template_name = "pharmacie/commandes/commande_deleted_list.html"
    context_object_name = "commandes_deleted"

    def get_queryset(self):
        return Commande.objects.deleted()  # Utiliser le manager personnalisé pour récupérer les commandes supprimées


# --- CRUD POUR STOCK ---

class GestionStockListView(ListView):
    model = Stock
    template_name = "pharmacie/stocks/gestion_stock_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        return Stock.objects.filter(deleted_at__isnull=True)  # Produits non supprimés
    
    
class StockListView(ListView):
    model = Stock
    template_name = "pharmacie/stocks/stock_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        return Stock.objects.filter(deleted_at__isnull=True)  # Produits non supprimés


class StockCreateView(CreateView):
    model = Stock
    form_class = StockForm
    template_name = "pharmacie/stocks/stock_form.html"
    success_url = reverse_lazy('pharmacie:stock_list')

    def form_valid(self, form):
        produit = form.cleaned_data['produit']
        
        # Vérifier si un Stock existe déjà pour ce produit
        if Stock.objects.filter(produit=produit).exists():
            form.add_error('produit', 'Ce produit a déjà un stock associé.')
            return self.form_invalid(form)

        return super().form_valid(form)


class StockDetailView(DetailView):
    model = Stock
    template_name = "pharmacie/stocks/stock_detail.html"
    context_object_name = "stock"

class StockUpdateView(UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "pharmacie/stocks/stock_form1.html"
    success_url = reverse_lazy('pharmacie:gestion_stock_list')  # Correction ici

class StockDeleteView(DeleteView):
    model = Stock
    template_name = "pharmacie/stocks/stock_confirm_delete.html"
    success_url = reverse_lazy('pharmacie:gestion_stock_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted_at = timezone.now()  # Marquer comme supprimé
        obj.save()
        return redirect(self.success_url)

class StockRestoreView(View):
    def get(self, request, pk):
        # Récupère le stock, y compris ceux supprimés logiquement
        stock = get_object_or_404(Stock.all_objects, pk=pk)  # Utilise all_objects pour inclure les objets supprimés
        stock.restore()  # Restaure le stock
        return redirect('pharmacie:gestion_stock_list')

class StockDeletedListView(ListView):
    model = Stock
    template_name = "pharmacie/stocks/stock_deleted_list.html"
    context_object_name = "stocks"

    def get_queryset(self):
        # Utilise 'deleted_at' pour filtrer les stocks supprimés
        return Stock.objects.deleted()


#  Liste des factures (remplace `liste_factures_pharmacie`)
@method_decorator(login_required, name='dispatch')
class FacturePharmacieListView(ListView):
    model = FacturePharmacie
    template_name = "pharmacie/factures/facture_list_pharmacie.html"
    context_object_name = "factures"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        context["factures_du_jour"] = FacturePharmacie.objects.filter(facture_date_time__date=today)
        return context
    
@method_decorator(login_required, name='dispatch')
class FacturePharmacieCaisseListView(ListView):
    model = FacturePharmacie
    template_name = "pharmacie/factures/caisse_facture_list_pharmacie.html"
    context_object_name = "factures"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        context["factures_du_jour"] = FacturePharmacie.objects.filter(facture_date_time__date=today)
        return context


@method_decorator(login_required, name='dispatch')
class FacturePharmacieRecepListView(ListView):
    model = FacturePharmacie
    template_name = "pharmacie/factures/recep_facture_list_pharmacie.html"
    context_object_name = "factures"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = now().date()
        context["factures_du_jour"] = FacturePharmacie.objects.filter(facture_date_time__date=today)
        return context


# Création d'une facture (remplace `creer_facturepharmacie`)
@method_decorator(login_required, name='dispatch')
class FacturePharmacieCreateView(CreateView):
    model = FacturePharmacie
    form_class = FacturePharmacieForm
    template_name = "pharmacie/factures/creer_facturepharmacie.html"
    success_url = reverse_lazy("pharmacie:liste_factures_pharmacie")

    def form_valid(self, form):
        facture = form.save(commit=False)
        facture.save_by = self.request.user.personnel  # Associe l'utilisateur connecté
        facture.save()

        formset = VenteFormSet(self.request.POST)
        if formset.is_valid():
            ventes = formset.save(commit=False)
            for vente in ventes:
                vente.facture = facture
                vente.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = VenteFormSet()
        return context

#  Modification d'une facture (remplace `modifier_facturePharmacie`)
@method_decorator(login_required, name='dispatch')
class FacturePharmacieUpdateView(UpdateView):
    model = FacturePharmacie
    form_class = FacturePharmacieFormUpdate
    template_name = "pharmacie/factures/facturepharmacie_update.html"
    success_url = reverse_lazy("pharmacie:liste_factures_pharmacie_caisse")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

#  Détail d'une facture (remplace `voir_facture_pharmacie`)
@method_decorator(login_required, name='dispatch')
class FacturePharmacieDetailView(DetailView):
    model = FacturePharmacie
    template_name = "pharmacie/factures/voir_facturepharmacie.html"
    context_object_name = "facture"

    def get_object(self):
        """ Récupère la facture par son numéro de facture """
        numero_facture = self.kwargs.get("numero_facture")
        return get_object_or_404(FacturePharmacie, numero_facture=numero_facture)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ventes"] = Vente.objects.filter(facture=self.object)
        return context