from django.urls import path
from .views import *

app_name = "rendezvous"

urlpatterns = [
    path("", RendezVousListView.as_view(), name="rendezvous_list"),
    path("ajouter/", RendezVousCreateView.as_view(), name="rendezvous_create"),
    path("<int:pk>/", RendezVousDetailView.as_view(), name="rendezvous_detail"),
    path("<int:pk>/modifier/", RendezVousUpdateView.as_view(), name="rendezvous_update"),
    path("<int:pk>/supprimer/", RendezVousDeleteView.as_view(), name="rendezvous_delete"),
    path("<int:pk>/restaurer/", RendezVousRestoreView.as_view(), name="rendezvous_restore"),
    path("corbeille/", RendezVousDeletedListView.as_view(), name="rendezvous_deleted_list"),
]
