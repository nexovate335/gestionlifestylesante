from django.urls import path
from .views import*


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', PersonnelListView.as_view(), name='personnel_list'),
    path('<int:pk>/', PersonnelDetailView.as_view(), name='personnel_detail'),
    path('<int:pk>/update/', PersonnelUpdateView.as_view(), name='personnel_update'),
    path('<int:pk>/delete/', PersonnelDeleteView.as_view(), name='personnel_delete'),
    path('<int:pk>/restore/', PersonnelRestoreView.as_view(), name='personnel_restore'),
    
    path('reception/', ReceptionView.as_view(), name='reception'),
    path('caisse/', CaisseView.as_view(), name='caisse'),
    path('caisse/garde/', CaisseGardeView.as_view(), name='caisse_garde'),
    path('pharmacie/', PharmacieView.as_view(), name='pharmacie'),
    path('pharmacieGarde/', PharmacieGardeView.as_view(), name='pharmaciegarde'),
    path('laboratoire/', LaboratoireView.as_view(), name='laboratoire'),
    path('blocoperatoire/', BlocOperatoireView.as_view(), name='blocoperatoire'),
    path('corbeille/', CorbeilleView.as_view(), name='corbeille'),
    path('gestionpharmacie/', GestionPharmacieView.as_view(), name='gestionpharmacie'),
    path('gestionpharmacieGarde/', GestionPharmacieGardeView.as_view(), name='gestionpharmaciegarde'),
    path('gestion/', GestionPersonnelView.as_view(), name='gestion_personnel'),
    path('paramedicale/', ParamedicaleView.as_view(), name='paramedicale'),
    path('Int-Docteur/', InterfaceDocteurView.as_view(), name='interface_docteur'),
    
    
]


