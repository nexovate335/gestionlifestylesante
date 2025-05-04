from django.urls import path
from .views import*

app_name = 'caisse_garde'

urlpatterns = [
   
    path("factures/recep/", FactureCaisseRecepGardeListView.as_view(), name="liste_factures_caisse_recep_garde"),
    path("factures/", FactureCaisseGardeListView.as_view(), name="liste_factures_caisse_garde"),
    path("factures/creer/", FactureCaisseGardeCreateView.as_view(), name="creer_facture_caisse_garde"),
    path("factures/paiement/<int:pk>/", FactureCaisseGardeUpdateView.as_view(), name="modifier_facture_caisse_garde"),
    path("factures/garde/<str:numero_facture>/", FactureCaisseGardeDetailView.as_view(), name="voir_facture_caisse_garde"),
    path("depenses/", AutresDepensesGardeListView.as_view(), name="autres_depenses_list_garde"),
    path("depenses/ajouter/", AutresDepensesGardeCreateView.as_view(), name="autres_depenses_create_garde"),
    path("depenses/modifier/<int:pk>/", AutresDepensesGardeUpdateView.as_view(), name="autres_depenses_update_garde"),
    path("depenses/supprimer/<int:pk>/", AutresDepensesGardeDeleteView.as_view(), name="autres_depenses_delete_garde"),
    path("rapports/", RapportJournalierCaisseGardeListView.as_view(), name="rapport_journalier_list_garde"),
    path("rapports/ajouter/", RapportJournalierCaisseGardeCreateView.as_view(), name="rapport_journalier_create_garde"),
    path("rapports/<int:pk>/modifier/", RapportJournalierCaisseGardeUpdateView.as_view(), name="rapport_journalier_update_garde"),
    path("rapports/<int:pk>/supprimer/", RapportJournalierCaisseGardeDeleteView.as_view(), name="rapport_journalier_delete_garde"),
]
