from django.urls import path
from .views import *

app_name = 'patient'  # Namespace

urlpatterns = [
    path('', PatientListView.as_view(), name='patient_list'),
    path('patient/', PatientLabListView.as_view(), name='patient_lab_list'),
    path('create/', PatientCreateView.as_view(), name='patient_create'),
    path('<int:pk>/', PatientDetailView.as_view(), name='patient_detail'),
    path('<int:pk>/patient/', PatientLabDetailView.as_view(), name='patient_lab_detail'),
    path('<int:pk>/update/', PatientUpdateView.as_view(), name='patient_update'),
    path('<int:pk>/update/patient/', PatientLabUpdateView.as_view(), name='patient_lab_update'),

    path('<int:pk>/delete/', PatientDeleteView.as_view(), name='patient_delete'),
    path('<int:pk>/restore/', PatientRestoreView.as_view(), name='patient_restore'), 
    path('deleted/', PatientDeletedListView.as_view(), name='patient_deleted_list'),
]
