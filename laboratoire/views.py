from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView, View
)
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import now
from patients.models import Patient
from .models import Examen, Resultat, ExamenCytologiePv, ExamenCytologieEcbu
from .forms import ExamenForm, ResultatForm, ExamenCytologiePvForm, ExamenCytologieEcbuForm

# ===========================================
# Views pour Examen
# ===========================================

# Liste des examens
class ExamenListView(ListView):
    model = Examen
    template_name = "laboratoire/examens/examen_list.html"
    context_object_name = "examens"
    
    def get_queryset(self):
       
        return Examen.objects.all().order_by('-date')


class ExamenLabListView(ListView):
    model = Examen
    template_name = "laboratoire/examens/examen_lab_list.html"
    context_object_name = "examens"
    
    def get_queryset(self):
        
        return Examen.objects.all().order_by('-date')


# Création d'un examen
class ExamenCreateView(CreateView):
    model = Examen
    form_class = ExamenForm
    template_name = "laboratoire/examens/examen_form.html"
    success_url = reverse_lazy("laboratoire:examen_lab_list")
    


# Détails d'un examen
class ExamenDetailView(DetailView):
    model = Examen
    template_name = "laboratoire/examens/examen_detail.html"
    context_object_name = "examen"


class ExamenLabDetailView(DetailView):
    model = Examen
    template_name = "laboratoire/examens/examen_lab_detail.html"
    context_object_name = "examen"

# Mise à jour d'un examen
class ExamenUpdateView(UpdateView):
    model = Examen
    form_class = ExamenForm
    template_name = "laboratoire/examens/examen_form1.html"
    success_url = reverse_lazy("laboratoire:examen_list")


class ExamenLabUpdateView(UpdateView):
    model = Examen
    form_class = ExamenForm
    template_name = "laboratoire/examens/examen_lab_form1.html"
    success_url = reverse_lazy("laboratoire:examen_lab_list")
    

# Suppression logique d'un examen
class ExamenDeleteView(DeleteView):
    model = Examen
    template_name = "laboratoire/examens/examen_confirm_delete.html"
    success_url = reverse_lazy("laboratoire:examen_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted_at = now()  # Suppression logique
        obj.save()
        return redirect(self.success_url)

# Restauration d'un examen supprimé
class ExamenRestoreView(View):
    def get(self, request, pk):
        examen = get_object_or_404(Examen.all_objects, pk=pk)
        examen.restore()  # Restauration de l'examen
        return redirect('laboratoire:examen_list')  # Redirection vers la liste des examens

# Liste des examens supprimés
class ExamenDeletedListView(ListView):
    model = Examen
    template_name = "laboratoire/examens/examen_deleted_list.html"
    context_object_name = "examens_deleted"

    def get_queryset(self):
        # Utiliser all_objects pour récupérer les objets avec une valeur dans deleted_at
        return Examen.all_objects.filter(deleted_at__isnull=False)  # Modifié ici pour récupérer les supprimés


# ===========================================
# Views pour Resultat
# ===========================================

# Liste des Résultats
class ResultatListView(ListView):
    model = Resultat
    template_name = "laboratoire/resultats/resultat_list.html"
    context_object_name = "resultats"

    def get_queryset(self):
        # Assurez-vous que vous récupérez tous les résultats
        return Resultat.objects.all().order_by('-date')
    
# Création d'un résultat
class ResultatCreateView(CreateView):
    model = Resultat
    form_class = ResultatForm
    template_name = "laboratoire/resultats/resultat_form.html"
    success_url = reverse_lazy("laboratoire:resultat_list")
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["patients"] = Patient.objects.all()
            return context

    def form_valid(self, form):
        patient_id = self.request.POST.get("patient")
        if patient_id:
            try:
                patient = Patient.objects.get(pk=patient_id)
                form.instance.patient = patient
                return super().form_valid(form)
            except Patient.DoesNotExist:
                form.add_error(None, "Patient introuvable.")
        else:
            form.add_error(None, "Veuillez sélectionner un patient.")
        return self.form_invalid(form)


    

# Détails d'un résultat
class ResultatDetailView(DetailView):
    model = Resultat
    template_name = "laboratoire/resultats/resultat_detail.html"
    context_object_name = "resultat"

# Mise à jour d'un résultat
class ResultatUpdateView(UpdateView):
    model = Resultat
    form_class = ResultatForm
    template_name = "laboratoire/resultats/resultat_form.html"
    success_url = reverse_lazy("laboratoire:resultat_list")
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["patients"] = Patient.objects.all()
            return context

    def form_valid(self, form):
        patient_id = self.request.POST.get("patient")
        if patient_id:
            try:
                patient = Patient.objects.get(pk=patient_id)
                form.instance.patient = patient
                return super().form_valid(form)
            except Patient.DoesNotExist:
                form.add_error(None, "Patient introuvable.")
        else:
            form.add_error(None, "Veuillez sélectionner un patient.")
        return self.form_invalid(form)


   
# Suppression logique d'un résultat
class ResultatDeleteView(DeleteView):
    model = Resultat
    template_name = "laboratoire/resultats/resultat_confirm_delete.html"
    success_url = reverse_lazy("laboratoire:resultat_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted_at = now()  # Marque le resultat comme supprimé
        obj.save()
        return redirect(self.success_url)
    
    
# Restauration d'un resultat supprimé
class ResultatRestoreView(View):
    def get(self, request, pk):
        resultat = get_object_or_404(Resultat.all_objects, pk=pk)
        resultat.restore()  # On restaure le resultat
        return redirect('laboratoire:resultat_list')  # Rediriger vers la liste des supprimés

# Liste des résultats supprimées
class ResultatDeletedListView(ListView):
    model = Resultat
    template_name = "laboratoire/resultats/resultat_deleted_list.html"
    context_object_name = "resultats_deleted"

    def get_queryset(self):
        # Utiliser le manager personnalisé pour récupérer les résultat supprimées
        return Resultat.objects.deleted()
        

# ===========================================
# Views pour Examen Cytologie PV
# ===========================================

# Liste des examens actifs
class ExamenCytologiePvListView(ListView):
    model = ExamenCytologiePv
    template_name = "laboratoire/examenscytopv/examencytopv_list.html"
    context_object_name = "examens"

    def get_queryset(self):
        return ExamenCytologiePv.objects.all().order_by('-date')

# Création d’un examen
class ExamenCytologiePvCreateView(CreateView):
    model = ExamenCytologiePv
    form_class = ExamenCytologiePvForm
    template_name = "laboratoire/examenscytopv/examencytopv_form.html"
    success_url = reverse_lazy("laboratoire:examencytopv_list")
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["patients"] = Patient.objects.all()
            return context

    def form_valid(self, form):
        patient_id = self.request.POST.get("patient")
        if patient_id:
            try:
                patient = Patient.objects.get(pk=patient_id)
                form.instance.patient = patient
                return super().form_valid(form)
            except Patient.DoesNotExist:
                form.add_error(None, "Patient introuvable.")
        else:
            form.add_error(None, "Veuillez sélectionner un patient.")
        return self.form_invalid(form)

# Détails d’un examen
class ExamenCytologiePvDetailView(DetailView):
    model = ExamenCytologiePv
    template_name = "laboratoire/examenscytopv/examencytopv_detail.html"
    context_object_name = "examen"
    

# Mise à jour d’un examen
class ExamenCytologiePvUpdateView(UpdateView):
    model = ExamenCytologiePv
    form_class = ExamenCytologiePvForm
    template_name = "laboratoire/examenscytopv/examencytopv_form.html"
    success_url = reverse_lazy("laboratoire:examencytopv_list")
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["patients"] = Patient.objects.all()
            return context

    def form_valid(self, form):
        patient_id = self.request.POST.get("patient")
        if patient_id:
            try:
                patient = Patient.objects.get(pk=patient_id)
                form.instance.patient = patient
                return super().form_valid(form)
            except Patient.DoesNotExist:
                form.add_error(None, "Patient introuvable.")
        else:
            form.add_error(None, "Veuillez sélectionner un patient.")
        return self.form_invalid(form)

# Suppression logique d’un examen
class ExamenCytologiePvDeleteView(DeleteView):
    model = ExamenCytologiePv
    template_name = "laboratoire/examenscytopv/examencytopv_confirm_delete.html"
    success_url = reverse_lazy("laboratoire:examencytopv_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted_at = now()
        obj.save()
        return redirect(self.success_url)

# Restauration d’un examen supprimé
class ExamenCytologiePvRestoreView(View):
    def get(self, request, pk):
        examen = get_object_or_404(ExamenCytologiePv.all_objects, pk=pk)
        examen.restore()
        return redirect("laboratoire:examencytopv_list")

# Liste des examens supprimés
class ExamenCytologiePvDeletedListView(ListView):
    model = ExamenCytologiePv
    template_name = "laboratoire/examenscytopv/examencytopv_deleted_list.html"
    context_object_name = "examens_deleted"

    def get_queryset(self):
        return ExamenCytologiePv.objects.deleted()



# ===========================================
# Views pour Examen Cytologie ECBU
# ===========================================

# Liste des examens cytologie/ecbu
class ExamenCytologieEcbuListView(ListView):
    model = ExamenCytologieEcbu
    template_name = "laboratoire/ecbu_cytologie/ecbu_cytologie_list.html"
    context_object_name = "examens"

    def get_queryset(self):
        return ExamenCytologieEcbu.objects.all().order_by('-date')

# Création d'un examen
class ExamenCytologieEcbuCreateView(CreateView):
    model = ExamenCytologieEcbu
    form_class = ExamenCytologieEcbuForm
    template_name = "laboratoire/ecbu_cytologie/ecbu_cytologie_form.html"
    success_url = reverse_lazy("laboratoire:ecbu_cytologie_list")
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["patients"] = Patient.objects.all()
            return context

    def form_valid(self, form):
        patient_id = self.request.POST.get("patient")
        if patient_id:
            try:
                patient = Patient.objects.get(pk=patient_id)
                form.instance.patient = patient
                return super().form_valid(form)
            except Patient.DoesNotExist:
                form.add_error(None, "Patient introuvable.")
        else:
            form.add_error(None, "Veuillez sélectionner un patient.")
        return self.form_invalid(form)

# Détail d'un examen
class ExamenCytologieEcbuDetailView(DetailView):
    model = ExamenCytologieEcbu
    template_name = "laboratoire/ecbu_cytologie/ecbu_cytologie_detail.html"
    context_object_name = "examen"

# Mise à jour d'un examen
class ExamenCytologieEcbuUpdateView(UpdateView):
    model = ExamenCytologieEcbu
    form_class = ExamenCytologieEcbuForm
    template_name = "laboratoire/ecbu_cytologie/ecbu_cytologie_form.html"
    success_url = reverse_lazy("laboratoire:ecbu_cytologie_list")
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["patients"] = Patient.objects.all()
            return context

    def form_valid(self, form):
        patient_id = self.request.POST.get("patient")
        if patient_id:
            try:
                patient = Patient.objects.get(pk=patient_id)
                form.instance.patient = patient
                return super().form_valid(form)
            except Patient.DoesNotExist:
                form.add_error(None, "Patient introuvable.")
        else:
            form.add_error(None, "Veuillez sélectionner un patient.")
        return self.form_invalid(form)

# Suppression logique d’un examen
class ExamenCytologieEcbuDeleteView(DeleteView):
    model = ExamenCytologieEcbu
    template_name = "laboratoire/ecbu_cytologie/ecbu_cytologie_confirm_delete.html"
    success_url = reverse_lazy("laboratoire:ecbu_cytologie_list")

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted_at = now()
        obj.save()
        return redirect(self.success_url)

# Restauration d’un examen supprimé
class ExamenCytologieEcbuRestoreView(View):
    def get(self, request, pk):
        examen = get_object_or_404(ExamenCytologieEcbu, pk=pk)
        examen.deleted_at = None
        examen.save()
        return redirect("laboratoire:ecbu_cytologie_list")

# Liste des examens supprimés
class ExamenCytologieEcbuDeletedListView(ListView):
    model = ExamenCytologieEcbu
    template_name = "laboratoire/ecbu_cytologie/ecbu_cytologie_deleted_list.html"
    context_object_name = "examens_deleted"

    def get_queryset(self):
        return ExamenCytologieEcbu.objects.filter(deleted_at__isnull=False)