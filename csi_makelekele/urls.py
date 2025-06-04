from django.urls import path
from .views import (
    PrestationListView,
    PrestationCreateView,
    PrestationDetailView,
    PrestationUpdateView,
    PrestationDeleteView,
    PrestationDeletedListView,
    PrestationRestoreView,
)

app_name = "prestation"

urlpatterns = [
    path('prestations/', PrestationListView.as_view(), name='prestation_list'),
    path('prestations/create/', PrestationCreateView.as_view(), name='prestation_create'),
    path('prestations/<int:pk>/', PrestationDetailView.as_view(), name='prestation_detail'),
    path('prestations/<int:pk>/update/', PrestationUpdateView.as_view(), name='prestation_update'),
    path('prestations/<int:pk>/delete/', PrestationDeleteView.as_view(), name='prestation_delete'),
    path('prestations/deleted/', PrestationDeletedListView.as_view(), name='prestation_deleted_list'),
    path('prestations/deleted/<int:pk>/restore/', PrestationRestoreView.as_view(), name='prestation_restore'),
]
