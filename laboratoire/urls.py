from django.urls import path
from .views import *

app_name = 'laboratoire'

urlpatterns = [
    # Examens
    path('', ExamenListView.as_view(), name='examen_list'),
    path('examens/create/', ExamenCreateView.as_view(), name='examen_create'),
    path('examens/<int:pk>/', ExamenDetailView.as_view(), name='examen_detail'),
    path('examens/<int:pk>/update/', ExamenUpdateView.as_view(), name='examen_update'),
    path('examens/<int:pk>/delete/', ExamenDeleteView.as_view(), name='examen_delete'),
    path('examens/<int:pk>/restore/', ExamenRestoreView.as_view(), name='examen_restore'),
    path('examens/deleted/', ExamenDeletedListView.as_view(), name='examen_deleted_list'),
    path('examens/lab', ExamenLabListView.as_view(), name='examen_lab_list'),
    path('examens/lab/<int:pk>/update/', ExamenLabUpdateView.as_view(), name='examen_lab_update'),
    path('examens/lab/<int:pk>/', ExamenLabDetailView.as_view(), name='examen_lab_detail'),
    
    # Résultats
    path('resultats/', ResultatListView.as_view(), name='resultat_list'),
    path('resultats/deleted/', ResultatDeletedListView.as_view(), name='resultat_deleted_list'),  # URL pour les examens supprimés
    path('resultat/create/', ResultatCreateView.as_view(), name='resultat_create'),
    path('resultat/<int:pk>/detail/', ResultatDetailView.as_view(), name='resultat_detail'),
    path('resultat/<int:pk>/update/', ResultatUpdateView.as_view(), name='resultat_update'),
    path('resultat/<int:pk>/delete/', ResultatDeleteView.as_view(), name='resultat_delete'),
    path('resultat/<int:pk>/restore/', ResultatRestoreView.as_view(), name='resultat_restore'),

    # Examen cytologie PV :
    path("examenscytopv/", ExamenCytologiePvListView.as_view(), name="examencytopv_list"),
    path("examenscytopv/ajouter/", ExamenCytologiePvCreateView.as_view(), name="examencytopv_create"),
    path("examenscytopv/<int:pk>/", ExamenCytologiePvDetailView.as_view(), name="examencytopv_detail"),
    path("examenscytopv/<int:pk>/modifier/", ExamenCytologiePvUpdateView.as_view(), name="examencytopv_update"),
    path("examenscytopv/<int:pk>/supprimer/", ExamenCytologiePvDeleteView.as_view(), name="examencytopv_delete"),
    path("examenscytopv/supprimes/", ExamenCytologiePvDeletedListView.as_view(), name="examencytopv_deleted_list"),
    path("examenscytopv/<int:pk>/restaurer/", ExamenCytologiePvRestoreView.as_view(), name="examencytopv_restore"),

    # Examen cytologie ECBU :
    path("ecbu_cytologie/", ExamenCytologieEcbuListView.as_view(), name="ecbu_cytologie_list"),
    path("ecbu_cytologie/ajouter/", ExamenCytologieEcbuCreateView.as_view(), name="ecbu_cytologie_create"),
    path("ecbu_cytologie/<int:pk>/", ExamenCytologieEcbuDetailView.as_view(), name="ecbu_cytologie_detail"),
    path("ecbu_cytologie/<int:pk>/modifier/", ExamenCytologieEcbuUpdateView.as_view(), name="ecbu_cytologie_update"),
    path("ecbu_cytologie/<int:pk>/supprimer/", ExamenCytologieEcbuDeleteView.as_view(), name="ecbu_cytologie_delete"),
    path("ecbu_cytologie/<int:pk>/restaurer/", ExamenCytologieEcbuRestoreView.as_view(), name="ecbu_cytologie_restore"),
    path("ecbu_cytologie/supprimes/", ExamenCytologieEcbuDeletedListView.as_view(), name="ecbu_cytologie_deleted_list"),


]
