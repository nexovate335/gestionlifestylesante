from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views import View
from .models import Personnel
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PersonnelForm,CustomUserCreationForm, LoginForm  
from .models import Personnel
from django.utils.decorators import method_decorator
from .decorators import fonction_required
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View


User = get_user_model()


# Dictionnaire de redirection en fonction du rôle de l'utilisateur
REDIRECTION_PAGES = {
    'Réceptioniste': 'reception',
    'Cassier(e)': 'caisse',
    'Pharmacien(ne)': 'pharmacieuser',
    'Laborantin(ne)': 'laboratoire',
    'Admin': 'blocoperatoire',
    'Admin': 'corbeille',
    'Gestionnaire-phamarcie': 'gestionpharmacie',
    'Admin': 'gestion_personnel',
    'Admin': 'interface_docteur',
    'Medecin': 'interface_docteur',
    'Infirmier(e)': 'paramedicale',
    'Aides-soignante': 'paramedicale', 
    'Medecin': 'paramedicale',
    'Infirmier(e)': 'caisse_gare',
    'Aides-soignante': 'caisse_garde', 
    
    
    
    
    

    
}
 
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'personnels/register.html'
    success_url = reverse_lazy('personnel_list')  # Redirige vers la page d'accueil après l'inscription

    def form_valid(self, form):
        # Sauvegarde l'utilisateur et connecte-le après l'inscription
        user = form.save()
        login(self.request, user)  # Connecte l'utilisateur après l'inscription
        return redirect(self.success_url)
    
    
def login_view(request):
    """Vue pour la connexion"""
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Vérifier si une URL de redirection existe (ex: accès à une page protégée)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)

                # Vérifier si l'utilisateur a un rôle
                if hasattr(user, 'personnel') and user.personnel:
                    fonction = getattr(user.personnel, 'fonction', None)
                    if fonction:
                        return redirect(REDIRECTION_PAGES.get(fonction, 'home'))

                # Redirection par défaut si aucun rôle n'est trouvé
                return redirect('home')
            else:
                messages.error(request, "Identifiants invalides. Veuillez réessayer.")
        else:
            messages.error(request, "Veuillez corriger les erreurs du formulaire.")

    return render(request, 'personnels/login.html', {'form': form})


def logout_view(request):
    """Vue pour la déconnexion"""
    logout(request)
    return redirect('home')

# Création d'une vue basée sur des classes pour le CRUD
class PersonnelListView(View):
    """Liste des membres du personnel."""
    def get(self, request):
        personnels = Personnel.objects.filter(deleted_at__isnull=True)
        return render(request, 'personnels/personnel/personnel_list.html', {'personnels': personnels})


class PersonnelUpdateView(View):
    """Mise à jour des informations d'un membre du personnel."""
    def get(self, request, pk):
        personnel = get_object_or_404(Personnel, pk=pk, deleted_at__isnull=True)
        form = PersonnelForm(instance=personnel)
        return render(request, 'personnels/personnel/personnel_form.html', {'form': form})

    def post(self, request, pk):
        personnel = get_object_or_404(Personnel, pk=pk, deleted_at__isnull=True)
        form = PersonnelForm(request.POST, instance=personnel)
        if form.is_valid():
            form.save()
            return redirect('personnel_list')
        return render(request, 'personnels/personnel/personnel_form.html', {'form': form})



class PersonnelDetailView(View):
    """Affichage des détails d'un membre du personnel."""
    def get(self, request, pk):
        # Recherche du personnel en filtrant les entrées non supprimées
        try:
            personnel = Personnel.objects.get(pk=pk, deleted_at__isnull=True)
        except Personnel.DoesNotExist:
            raise Http404("Le personnel avec cet ID n'existe pas ou a été supprimé.")
        
        return render(request, 'personnels/personnel/personnel_detail.html', {'personnel': personnel})


class PersonnelDeleteView(View):
    """Suppression logique d'un membre du personnel."""
    def post(self, request, pk):
        personnel = get_object_or_404(Personnel, pk=pk, deleted_at__isnull=True)
        personnel.delete()
        return redirect('personnel_list')  # Rediriger après suppression

# Restauration d'un personnel
class PersonnelRestoreView(View):
    def post(self, request, pk):
        personnel = get_object_or_404(Personnel.all_objects.filter(deleted_at__isnull=False), pk=pk)
        personnel.restore()
        return redirect('personnel_list')

# Restauration d'un personnel
class PersonnelRestoreView(View):
    def post(self, request, pk):
        personnel = get_object_or_404(Personnel.all_objects.filter(deleted_at__isnull=False), pk=pk)
        personnel.restore()
        return redirect('personnel_deleted_list')  # Rediriger vers la liste des supprimés après restauration
   
# Liste des personnels supprimés
class PersonnelDeletedListView(View):
    model = Personnel
    template_name = "personnels/personnel/personnel_deleted_list.html"
    context_object_name = "deleted_personnels"

    def get(self, request):
        deleted_personnels = Personnel.all_objects.filter(deleted_at__isnull=False)
        return render(request, 'personnels/personnel/personnel_deleted_list.html', {'deleted_personnels': deleted_personnels})
    

@method_decorator([login_required, fonction_required('Admin')], name='dispatch')
class CorbeilleView(View):
    def get(self, request):
        personnel = Personnel.objects.first()  
        return render(request, 'corbeille.html')
    
#gestion pharmacie  
@method_decorator([login_required, fonction_required('Admin')], name='dispatch')
class GestionPersonnelView(View):
    def get(self, request):
        applications_gestion_personnel = [
            {'nom': 'Personnels', 'url': 'personnel_list'},
            {'nom': 'Créer un compte', 'url': 'register'}, 
             
    
            
        ]
        return render(request, 'personnels/gestionpersonnel.html', {'applications': applications_gestion_personnel})

    
#gestion pharmacie
@method_decorator([login_required, fonction_required('Gestionnaire-phamarcie')], name='dispatch')
class GestionPharmacieView(View):
    def get(self, request):
        applications_gestion_pharmacie = [
            {'nom': 'Produits', 'url': 'pharmacie:produit_list'}, 
            {'nom': 'Fournisseurs', 'url': 'pharmacie:fournisseur_list'}, 
            {'nom': 'Commandes', 'url': 'pharmacie:commande_list'},    
            {'nom': 'Stocks', 'url': 'pharmacie:gestion_stock_list'},  
        ]  
        return render(request, 'pharmacie/gestionpharmacie.html' ,{'applications': applications_gestion_pharmacie})

#Recepteur
@method_decorator([login_required, fonction_required('Réceptioniste')], name='dispatch')
class ReceptionView(View):
    def get(self, request):
        # Liste des applications à afficher
        applications_reception = [
            {'nom': 'Patients', 'url': 'patient:patient_list'},  
            {'nom': 'Pansement', 'url': 'pansement:pansement_list'},  
            {'nom': 'Consultation', 'url': 'consultation:consultation_list'},  
            {'nom': 'Hospitalisation', 'url': 'hospitalisation:hospitalisation_list'},  
            {'nom': 'Echographie', 'url': 'echographie:echographie_list'},  
            {'nom': 'Vaccin', 'url': 'vaccin:vaccin_list'},  
            {'nom': 'Viol', 'url': 'viol:viol_list'},  
            {'nom': 'MTO', 'url': 'mto:mto_list'},
             {'nom': 'Examens', 'url': 'laboratoire:examen_list'},
            {'nom': 'Bloc Operatoire', 'url': 'blocoperatoire:blocoperatoire_list_recep'},
            {'nom': 'Rendez-vous', 'url': 'rendezvous:rendezvous_list'},
            {'nom': 'Factures  caisse', 'url': 'caisse:liste_factures_caisse_recep'}, 
            {'nom': 'Factures caisse de Garde', 'url': 'caisse_garde:liste_factures_caisse_recep_garde'},
            {'nom': 'Factures Pharmacie', 'url': 'pharmacie:liste_factures_pharmacie_recep'},  
            {'nom': 'Factures Pharmaie de Garde', 'url': 'pharmacie_garde:liste_factures_phgarde_recep'},  
              
             
              
            
              
        ]

        return render(request, 'reception/reception.html', {'applications': applications_reception})

#Caisse
@method_decorator([login_required, fonction_required('Cassier(e)')], name='dispatch')
class CaisseView(View):
    def get(self, request):
        applications_caisse = [
            {'nom': 'Facture Hôpital', 'url': 'caisse:liste_factures_caisse'},  
            {'nom': 'Facture Pharmacie', 'url': 'pharmacie:liste_factures_pharmacie_caisse'}, 
             
            {'nom': 'Autre Depenses', 'url': 'caisse:autres_depenses_list'},
            {'nom': 'Rapports Journaliers de Caisse', 'url': 'caisse:rapport_journalier_list'},
                

        ]
        print("Applications caisse :", applications_caisse)  # Debug

        return render(request, 'caisse/caisse.html', {'applications': applications_caisse})

#Caisse de garde
@method_decorator([login_required, fonction_required('Infirmier(e)','Aides-soignante')], name='dispatch')
class CaisseGardeView(View):
    def get(self, request):
        applications_caisse_garde = [
            {'nom': 'Facture Hôpital de Garde ', 'url': 'caisse_garde:liste_factures_caisse_garde'},  
            {'nom': 'Facture Pharmacie de Garde', 'url': 'pharmacie_garde:liste_factures_phgarde_caisse'},  
             
            {'nom': 'Autre Depenses de Garde', 'url': 'caisse_garde:autres_depenses_list_garde'},
            {'nom': 'Rapports Journaliers de Caisse de Garde', 'url': 'caisse_garde:rapport_journalier_list_garde'},
                

        ]
        print("Applications caisse de garde :", applications_caisse_garde)  # Debug

        return render(request, 'caisse_garde/caisse_garde.html', {'applications_garde': applications_caisse_garde})


#Pharmacie
@method_decorator([login_required, fonction_required('Pharmacien(ne)', 'Gestionnaire-phamarcie')], name='dispatch')
class PharmacieView(View):
    def get(self, request):
        applications_pharmacie = [    
            {'nom': 'Stocks', 'url':  'pharmacie:stock_list'},
            {'nom': 'Factures', 'url': 'pharmacie:liste_factures_pharmacie'},    
        ]
        print("Applications pharmacie : ", applications_pharmacie)  # Debug

        return render(request, 'pharmacie/pharmacie.html', {'applications': applications_pharmacie})
    
#Laboratoire
@method_decorator([login_required, fonction_required('Laborantin(ne)')], name='dispatch')
class LaboratoireView(View):
    def get(self, request):
        # Liste des fonctionnalités du laboratoire
        applications_laboratoire = [
            {'nom': 'Patients', 'url': 'patient:patient_lab_list'},  
            {'nom': 'Examen', 'url': 'laboratoire:examen_lab_list'},
            {'nom': 'Résultat', 'url': 'laboratoire:resultat_list'},
            {'nom': 'Examen Cytologie PV', 'url': 'laboratoire:examencytopv_list'},
            {'nom': 'Examen Cytologie ECBU', 'url': 'laboratoire:ecbu_cytologie_list'},

        ]

        return render(request, 'laboratoire/laboratoire.html', {'applications': applications_laboratoire})

#BlocOperatoire
@method_decorator([login_required, fonction_required('Admin')], name='dispatch')
class BlocOperatoireView(View):
    def get(self, request):
        applications_blocoperatoire = [
            {'nom': 'BlocOperatoire', 'url': 'blocoperatoire:blocoperatoire_list'},
        ]

        return render(request, 'blocoperatoire/blocoperatoire.html', {'applications': applications_blocoperatoire})
    

#Pharmacie
@method_decorator([login_required, fonction_required('Pharmacien(ne)', 'Gestionnaire-phamarcie')], name='dispatch')
class PharmacieGardeView(View):
    def get(self, request):
        applications_pharmacie_garde = [    
            {'nom': 'Stocks pharmacie de garde', 'url':  'pharmacie_garde:phgardestock_list'},
            {'nom': 'Factures pharmacie de garde', 'url': 'pharmacie_garde:liste_factures_phgarde'},    
        ]
        print("Applications pharmacie_garde : ", applications_pharmacie_garde)  # Debug

        return render(request, 'pharmacie_garde/pharmacieGarde.html', {'applications': applications_pharmacie_garde})



#gestion pharmacie
@method_decorator([login_required, fonction_required('Gestionnaire-phamarcie')], name='dispatch')
class GestionPharmacieGardeView(View):
    def get(self, request):
        applications_gestion_pharmacie_garde = [
            {'nom': 'Produits', 'url': 'pharmacie_garde:phgardeproduit_list'}, 
            {'nom': 'Commandes', 'url': 'pharmacie_garde:phgardecommande_list'},    
            {'nom': 'Stocks', 'url': 'pharmacie_garde:phgardegestion_stock_list'},  
        ]  
        return render(request, 'pharmacie_garde/gestionpharmacieGarde.html' ,{'applications': applications_gestion_pharmacie_garde})


@method_decorator([login_required, fonction_required('Infirmier(e)','Aides-soignante')], name='dispatch')
class ParamedicaleView(View):
    def get(self, request):
        applications_consultation = [
            
             {'nom': 'Suite Consultation', 'url': 'consultation:suiteconsultation_list'}, 
            
        ]
        return render(request, 'paramedicale/paramedicale.html', {'applications': applications_consultation})
    
    
@method_decorator([login_required, fonction_required('Admin','Medecin')], name='dispatch')
class InterfaceDocteurView(View):
    def get(self, request):
        suivis = [
            
            {'nom': 'Suivi Consultation  par le medecin', 'url': 'consultation:suiviconsultation_list'},
            {'nom': 'Traitement par rapport à une consultation', 'url': 'consultation:ordonnance_list'},
            
        ]
        return render(request, 'interface_docteur/interface_docteur.html', {'suivis': suivis})
