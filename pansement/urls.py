from django.urls import path
from .views import *

app_name = 'pansement'

urlpatterns = [
    path('', PansementListView.as_view(), name='pansement_list'),
    path('create/', PansementCreateView.as_view(), name='pansement_create'),
    path('<int:pk>/', PansementDetailView.as_view(), name='pansement_detail'),  # Assurez-vous que cette ligne est présente
    path('<int:pk>/update/', PansementUpdateView.as_view(), name='pansement_update'),
    path('<int:pk>/delete/', PansementDeleteView.as_view(), name='pansement_delete'),
    path('<int:pk>/restore/', PansementRestoreView.as_view(), name='pansement_restore'),
    path('deleted/', PansementDeletedListView.as_view(), name='pansement_deleted_list'),
    path('autocomplete/patients/',patient_autocomplete_api, name='patient-autocomplete-api'),
]
