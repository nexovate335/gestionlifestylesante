from django.urls import path
from .views import*

app_name = 'caisse'

urlpatterns = [
   
    path("factures/recep/", FactureCaisseRecepListView.as_view(), name="liste_factures_caisse_recep"),
    path("factures/", FactureCaisseListView.as_view(), name="liste_factures_caisse"),
    path("factures/creer/", FactureCaisseCreateView.as_view(), name="creer_facture_caisse"),
    path("factures/paiement/<int:pk>/", FactureCaisseUpdateView.as_view(), name="modifier_facture_caisse"),
    path("factures/<str:numero_facture>/", FactureCaisseDetailView.as_view(), name="voir_facture_caisse"),
    path("depenses/", AutresDepensesListView.as_view(), name="autres_depenses_list"),
    path("depenses/ajouter/", AutresDepensesCreateView.as_view(), name="autres_depenses_create"),
    path("depenses/modifier/<int:pk>/", AutresDepensesUpdateView.as_view(), name="autres_depenses_update"),
    path("depenses/supprimer/<int:pk>/", AutresDepensesDeleteView.as_view(), name="autres_depenses_delete"),
    path("rapports/", RapportJournalierCaisseListView.as_view(), name="rapport_journalier_list"),
    path("rapports/ajouter/", RapportJournalierCaisseCreateView.as_view(), name="rapport_journalier_create"),
    path("rapports/<int:pk>/modifier/", RapportJournalierCaisseUpdateView.as_view(), name="rapport_journalier_update"),
    path("rapports/<int:pk>/supprimer/", RapportJournalierCaisseDeleteView.as_view(), name="rapport_journalier_delete"),
]
