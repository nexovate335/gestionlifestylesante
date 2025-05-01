from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.utils.timezone import now
from .models import Patient
from .forms import PatientForm, PatientLabForm

# Liste des patients actifs
class PatientListView(ListView):
    model = Patient
    template_name = "patient/patients/patient_list.html"
    context_object_name = "patients"

    def get_queryset(self):
        return Patient.objects.filter(deleted_at__isnull=True)  # Patients non supprimés


class PatientLabListView(ListView):
    model = Patient
    template_name = "patient/patients/patient_lab_list.html"
    context_object_name = "patients"

    def get_queryset(self):
        return Patient.objects.filter(deleted_at__isnull=True)  # Patients non supprimés

# Création d'un patient
class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "patient/patients/patient_form.html"
    success_url = reverse_lazy("patient:patient_list")

    def form_valid(self, form):
        # Assure-toi que le formulaire est valide
        if form.is_valid():
            patient = form.save(commit=False)
            patient.groupe_sanguin = self.request.POST.get("groupe_sanguin", "")  # Récupérer le groupe sanguin
            patient.sexe = self.request.POST.get("sexe", "")  # Récupérer le sexe du patient
            patient.save()
            return redirect(self.success_url)
        else:
            # Si le formulaire n'est pas valide, retourne un message d'erreur
            return self.form_invalid(form)

# Détails d'un patient
class PatientDetailView(DetailView):
    model = Patient
    template_name = "patient/patients/patient_detail.html"
    context_object_name = "patient"


class PatientLabDetailView(DetailView):
    model = Patient
    template_name = "patient/patients/patient_lab_detail.html"
    context_object_name = "patient"

# Mise à jour d'un patient
class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "patient/patients/patient_form.html"
    success_url = reverse_lazy("patient:patient_list")


class PatientLabUpdateView(UpdateView):
    model = Patient
    form_class = PatientLabForm
    template_name = "patient/patients/patient_lab_form.html"
    success_url = reverse_lazy("patient:patient_lab_list")

# Suppression d'un patient (marquer comme supprimé)
class PatientDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        patient = get_object_or_404(Patient, pk=pk)
        patient.delete()  # Utilise la méthode delete() définie dans le modèle
        return redirect(reverse_lazy("patient:patient_list"))

# Restauration d'un patient supprimé
class PatientRestoreView(View):
    def get(self, request, pk):
        patient = get_object_or_404(Patient.all_objects, pk=pk)  #  Récupère même les supprimés
        patient.restore()  #  Restaure le patient
        return redirect(reverse_lazy("patient:patient_deleted_list"))

# Liste des patients supprimés
class PatientDeletedListView(ListView):
    model = Patient
    template_name = "patient/patients/patient_deleted_list.html"
    context_object_name = "patients_deleted"

    def get_queryset(self):
        return Patient.objects.deleted()  # Récupère uniquement les patients supprimés
