from django.urls import path
from . import views

app_name = "mto"  # Nom de l'application pour la gestion des Mtos

urlpatterns = [
    path('', views.MtoListView.as_view(), name='mto_list'),
    path('create/', views.MtoCreateView.as_view(), name='mto_create'),
    path('<int:pk>/', views.MtoDetailView.as_view(), name='mto_detail'),
    path('<int:pk>/update/', views.MtoUpdateView.as_view(), name='mto_update'),
    path('<int:pk>/delete/', views.MtoDeleteView.as_view(), name='mto_delete'),
    path('<int:pk>/restore/', views.MtoRestoreView.as_view(), name='mto_restore'),
    path('deleted/', views.MtoDeletedListView.as_view(), name='mto_deleted_list'),
]
