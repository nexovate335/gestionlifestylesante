from django.urls import path
from .views import *

app_name = 'consultation'  # Définition du namespace pour cette application

urlpatterns = [
    path('', ConsultationListView.as_view(), name='consultation_list'),
    path('suite-con/', SuiteConsultationListView.as_view(), name='suiteconsultation_list'),
    path('suivi-con', SuiviConsultationListView.as_view(), name='suiviconsultation_list'),
    path('create/', ConsultationCreateView.as_view(), name='consultation_create'),
    path('<int:pk>/', ConsultationDetailView.as_view(), name='consultation_detail'),
    path('<int:pk>/suite-con/', SuiteConsultationDetailView.as_view(), name='suiteconsultation_detail'),
    path('<int:pk>/suivi-con/', SuiviConsultationDetailView.as_view(), name='suiviconsultation_detail'),
    path('<int:pk>/update/', ConsultationUpdateView.as_view(), name='consultation_update'),
    path('<int:pk>/update/suite-com', SuiteConsultationUpdateView.as_view(), name='suiteconsultation_update'),
    path('<int:pk>/update/suivi-con', SuiviConsultationUpdateView.as_view(), name='suiviconsultation_update'),
    path('<int:pk>/delete/', ConsultationDeleteView.as_view(), name='consultation_delete'),
    path('<int:pk>/restore/', ConsultationRestoreView.as_view(), name='consultation_restore'),
    path('deleted/', ConsultationDeletedListView.as_view(), name='consultation_deleted_list'),
    
    path('ordonnances/', OrdonnanceListView.as_view(), name='ordonnance_list'),
    path('ordonnances/nouvelle/', OrdonnanceCreateView.as_view(), name='ordonnance_create'),
    path('ordonnances/<int:pk>/', OrdonnanceDetailView.as_view(), name='ordonnance_detail'),
    path('ordonnances/<int:pk>/modifier/', OrdonnanceUpdateView.as_view(), name='ordonnance_update'),
    path('ordonnances/<int:pk>/supprimer/', OrdonnanceDeleteView.as_view(), name='ordonnance_delete'),
]
