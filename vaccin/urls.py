from django.urls import path
from .views import *

app_name = "vaccin"

urlpatterns = [
    path('', VaccinListView.as_view(), name="vaccin_list"),
    path('create/', VaccinCreateView.as_view(), name="vaccin_create"),
    path('<int:pk>/', VaccinDetailView.as_view(), name="vaccin_detail"),
    path('<int:pk>/update/', VaccinUpdateView.as_view(), name="vaccin_update"),
    path('<int:pk>/delete/', VaccinDeleteView.as_view(), name="vaccin_delete"),
    path('deleted/', VaccinDeletedListView.as_view(), name="vaccin_deleted_list"),
    path('<int:pk>/restore/', VaccinRestoreView.as_view(), name="vaccin_restore"),
]
