from django.urls import path
from .views import *

app_name="viol"

urlpatterns = [
    path('', ViolListView.as_view(), name='viol_list'),  # Liste des viols actifs
    path('create/', ViolCreateView.as_view(), name='viol_create'),  # Création d'un viol
    path('<int:pk>/', ViolDetailView.as_view(), name='viol_detail'),  # Détails d'un viol
    path('<int:pk>/edit/', ViolUpdateView.as_view(), name='viol_update'),  # Mise à jour d'un viol
    path('<int:pk>/delete/', ViolDeleteView.as_view(), name='viol_delete'),  # Suppression logique d'un viol
    path('<int:pk>/restore/', ViolRestoreView.as_view(), name='viol_restore'),  # Restauration d'un viol
    path('deleted/', ViolDeletedListView.as_view(), name='viol_deleted_list'),  # Liste des viols supprimés (corbeille)
]
