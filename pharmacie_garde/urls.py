from django.urls import path
from .views import *

app_name = 'pharmacie_garde'

urlpatterns = [
    
    
    # URLs pour Produits
    path("produits/", PhGardeProduitListView.as_view(), name="phgardeproduit_list"),
    path("produits/create/", PhGardeProduitCreateView.as_view(), name="phgardeproduit_create"),
    path('produits/<int:pk>/', PhGardeProduitDetailView.as_view(), name='phgardeproduit_detail'),
    path("produits/<int:pk>/update/", PhGardeProduitUpdateView.as_view(), name="phgardeproduit_update"),
    path("produits/<int:pk>/delete/", PhGardeProduitDeleteView.as_view(), name="phgardeproduit_delete"),
    path("produits/<int:pk>/restore/", PhGardeProduitRestoreView.as_view(), name="phgardeproduit_restore"),
    path("produits/deleted/", PhGardeProduitDeletedListView.as_view(), name="phgardeproduit_deleted_list"),

    

    # URLs pour Commandes
    path("commandes/", PhGardeCommandeListView.as_view(), name="phgardecommande_list"),
    path("commandes/create/", PhGardeCommandeCreateView.as_view(), name="phgardecommande_create"),
    path("commandes/<int:pk>/", PhGardeCommandeDetailView.as_view(), name="phgardecommande_detail"),
    path("commandes/<int:pk>/update/", PhGardeCommandeUpdateView.as_view(), name="phgardecommande_update"),
    path("commandes/<int:pk>/delete/", PhGardeCommandeDeleteView.as_view(), name="phgardecommande_delete"),
    path("commandes/<int:pk>/restore/", PhGardeCommandeRestoreView.as_view(), name="phgardecommande_restore"),
    path("commandes/deleted/", PhGardeCommandeDeletedListView.as_view(), name="phgardecommande_deleted_list"),


    # URLs pour Stocks
    path("stocks/gestion", PhGardeGestionStockListView.as_view(), name="phgardegestion_stock_list"),
    path("stocks/", PhGardeStockListView.as_view(), name="phgardestock_list"),
    path("stocks/create/", PhGardeStockCreateView.as_view(), name="phgardestock_create"),
    path("stocks/<int:pk>/", PhGardeStockDetailView.as_view(), name="phgardestock_detail"),  # Détails du stock
    path("stocks/<int:pk>/update/", PhGardeStockUpdateView.as_view(), name="phgardestock_update"),
    path("stocks/<int:pk>/delete/", PhGardeStockDeleteView.as_view(), name="phgardestock_delete"),
    path("stocks/<int:pk>/restore/", PhGardeStockRestoreView.as_view(), name="phgardestock_restore"),
    path("stocks/deleted/", PhGardeStockDeletedListView.as_view(), name="phgardestock_deleted_list"),

    
    # URLs pour Factures Pharmacie
    path("factures/caisse/", PhGardeFacturePharmacieCaisseListView.as_view(), name="liste_factures_phgarde_caisse"),
    path("factures/", PhGardeFacturePharmacieListView.as_view(), name="liste_factures_phgarde"),
    path("factures/creer/", PhGardeFacturePharmacieCreateView.as_view(), name="creer_facture_phgarde"),
    path("factures/<int:pk>/paiement/", PhGardeFacturePharmacieUpdateView.as_view(), name="modifier_facture_phgarde"),
    path("factures/<str:numero_facture>/", PhGardeFacturePharmacieDetailView.as_view(), name="voir_facture_phgarde"),

]

  