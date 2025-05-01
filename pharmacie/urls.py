from django.urls import path
from .views import *

app_name = 'pharmacie'

urlpatterns = [
    
    # URLs pour Produits
    path("produits/", ProduitListView.as_view(), name="produit_list"),
    path("produits/create/", ProduitCreateView.as_view(), name="produit_create"),
    path('produits/<int:pk>/', ProduitDetailView.as_view(), name='produit_detail'),
    path("produits/<int:pk>/update/", ProduitUpdateView.as_view(), name="produit_update"),
    path("produits/<int:pk>/delete/", ProduitDeleteView.as_view(), name="produit_delete"),
    path("produits/<int:pk>/restore/", ProduitRestoreView.as_view(), name="produit_restore"),
    path("produits/deleted/", ProduitDeletedListView.as_view(), name="produit_deleted_list"),


    # URLs pour Fournisseurs
    path("fournisseurs/", FournisseurListView.as_view(), name="fournisseur_list"),
    path("fournisseurs/create/", FournisseurCreateView.as_view(), name="fournisseur_create"),
    path("fournisseurs/<int:pk>/", FournisseurDetailView.as_view(), name="fournisseur_detail"),
    path("fournisseurs/<int:pk>/update/", FournisseurUpdateView.as_view(), name="fournisseur_update"),
    path("fournisseurs/<int:pk>/delete/", FournisseurDeleteView.as_view(), name="fournisseur_delete"),
    path("fournisseurs/<int:pk>/restore/", FournisseurRestoreView.as_view(), name="fournisseur_restore"),
    path("fournisseurs/deleted/", FournisseurDeletedListView.as_view(), name="fournisseur_deleted_list"),

    # URLs pour Commandes
    path("commandes/", CommandeListView.as_view(), name="commande_list"),
    path("commandes/create/", CommandeCreateView.as_view(), name="commande_create"),
    path("commandes/<int:pk>/", CommandeDetailView.as_view(), name="commande_detail"),
    path("commandes/<int:pk>/update/", CommandeUpdateView.as_view(), name="commande_update"),
    path("commandes/<int:pk>/delete/", CommandeDeleteView.as_view(), name="commande_delete"),
    path("commandes/<int:pk>/restore/", CommandeRestoreView.as_view(), name="commande_restore"),
    path("commandes/deleted/", CommandeDeletedListView.as_view(), name="commande_deleted_list"),


    # URLs pour Stocks
    path("stocks/gestion", GestionStockListView.as_view(), name="gestion_stock_list"),
    path("stocks/", StockListView.as_view(), name="stock_list"),
    path("stocks/create/", StockCreateView.as_view(), name="stock_create"),
    path("stocks/<int:pk>/", StockDetailView.as_view(), name="stock_detail"),  # Détails du stock
    path("stocks/<int:pk>/update/", StockUpdateView.as_view(), name="stock_update"),
    path("stocks/<int:pk>/delete/", StockDeleteView.as_view(), name="stock_delete"),
    path("stocks/<int:pk>/restore/", StockRestoreView.as_view(), name="stock_restore"),
    path("stocks/deleted/", StockDeletedListView.as_view(), name="stock_deleted_list"),

    
    # URLs pour Factures Pharmacie
    path("factures/caisse/", FacturePharmacieCaisseListView.as_view(), name="liste_factures_pharmacie_caisse"),
    path("factures/", FacturePharmacieListView.as_view(), name="liste_factures_pharmacie"),
    path("factures/creer/", FacturePharmacieCreateView.as_view(), name="creer_facture_pharmacie"),
    path("factures/<int:pk>/paiement/", FacturePharmacieUpdateView.as_view(), name="modifier_facture_Pharmacie"),
    path("factures/<str:numero_facture>/", FacturePharmacieDetailView.as_view(), name="voir_facture_pharmacie"),

]

  