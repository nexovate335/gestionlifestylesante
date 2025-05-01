from django.urls import path
from .views import *

app_name = "hospitalisation"

urlpatterns = [
    path('', HospitalisationListView.as_view(), name='hospitalisation_list'),
    path('create/', HospitalisationCreateView.as_view(), name='hospitalisation_create'),
    path('<int:pk>/', HospitalisationDetailView.as_view(), name='hospitalisation_detail'),
    path('<int:pk>/update/', HospitalisationUpdateView.as_view(), name='hospitalisation_update'),
    path('<int:pk>/delete/', HospitalisationDeleteView.as_view(), name='hospitalisation_delete'),
    path('<int:pk>/restore/', HospitalisationRestoreView.as_view(), name='hospitalisation_restore'),
    path('deleted/', HospitalisationDeletedListView.as_view(), name='hospitalisation_deleted_list'),  # Correction ici
]
