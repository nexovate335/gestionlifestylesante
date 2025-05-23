from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView, View
)
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import now
from django.urls import reverse 
from .models import Consultation, Ordonnance, Traitement
from .forms import ConsultationForm, SuiteConsultationForm, SuiviConsultationForm, OrdonnanceForm, TraitementForm, TraitementFormSet
from patients.models import Patient
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from personnels.mixins import SaveByPersonnelMixin

# Liste des consultations
class ConsultationListView(ListView):
    model = Consultation
    template_name = "consultation/consultations/consultation_list.html"
    context_object_name = "consultations"

    def get_queryset(self):
        return Consultation.objects.filter(deleted_at__isnull=True)  # Récupère uniquement les consultations actives


class SuiteConsultationListView(ListView):
    model = Consultation
    template_name = "paramedicale/suiteconsultation_list.html"
    context_object_name = "consultations"

    def get_queryset(self):
        return Consultation.objects.filter(deleted_at__isnull=True)  # Récupère uniquement les consultations actives


class SuiviConsultationListView(ListView):
    model = Consultation
    template_name = "interface_docteur/suiviconsultation_list.html"
    context_object_name = "consultations"

    def get_queryset(self):
        return Consultation.objects.filter(deleted_at__isnull=True)  # Récupère uniquement les consultations actives


# Création d'une consultation   
class ConsultationCreateView(LoginRequiredMixin, SaveByPersonnelMixin, CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = "consultation/consultations/consultation_form.html"
    success_url = reverse_lazy('consultation:consultation_list')

    
# Détails d'une consultation
class ConsultationDetailView(DetailView):
    model = Consultation
    template_name = "consultation/consultations/consultation_detail.html"
    context_object_name = "consultation"


class SuiteConsultationDetailView(DetailView):
    model = Consultation
    template_name = "paramedicale/suiteconsultation_detail.html"
    context_object_name = "consultation"


class SuiviConsultationDetailView(DetailView):
    model = Consultation
    template_name = "interface_docteur/suiviconsultation_detail.html"
    context_object_name = "consultation"

# Mise à jour d'une consultation
class ConsultationUpdateView(UpdateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = "consultation/consultations/consultation_form1.html"

    def get_success_url(self):
        return reverse('consultation:consultation_detail', kwargs={'pk': self.object.pk})


class SuiteConsultationUpdateView(UpdateView):
    model = Consultation
    form_class = SuiteConsultationForm
    template_name = "paramedicale/suiteconsultation_form1.html"

    def get_success_url(self):
        return reverse('consultation:suiteconsultation_detail', kwargs={'pk': self.object.pk})


class SuiviConsultationUpdateView(UpdateView):
    model = Consultation
    form_class = SuiviConsultationForm
    template_name = "interface_docteur/suiviconsultation_form1.html"

    def get_success_url(self):
        return reverse('consultation:suiviconsultation_detail', kwargs={'pk': self.object.pk})

# Suppression logique d'une consultation
class ConsultationDeleteView(DeleteView):
    model = Consultation
    template_name = "consultation/consultations/consultation_confirm_delete.html"
    success_url = "/consultation/"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.deleted_at = now()
        obj.save()
        return redirect(self.success_url)


# Restauration d'une consultation supprimée
class ConsultationRestoreView(View):
    def get(self, request, pk):
        consultation = get_object_or_404(Consultation.all_objects, pk=pk)
        consultation.restore()
        return redirect("/consultation/")

class ConsultationDeletedListView(ListView):
    model = Consultation
    template_name = "consultation/consultations/consultation_deleted_list.html"
    context_object_name = "consultation_deleted"

    def get_queryset(self):
        return Consultation.objects.deleted()  # Récupère uniquement les consultations supprimées



class OrdonnanceCreateView(View):
    template_name = 'interface_docteur/ordonnances/ordonnance_form.html'

    def get(self, request):
        ordonnance_form = OrdonnanceForm()
        formset = TraitementFormSet(prefix='traitement')
        return render(request, self.template_name, {
            'ordonnance_form': ordonnance_form,
            'formset': formset
        })

    def post(self, request):
        ordonnance_form = OrdonnanceForm(request.POST)
        formset = TraitementFormSet(request.POST, prefix='traitement')

        if ordonnance_form.is_valid() and formset.is_valid():
            ordonnance = ordonnance_form.save()
            traitements = formset.save(commit=False)
            for traitement in traitements:
                traitement.ordonnance = ordonnance
                traitement.save()
            formset.save_m2m()
            return redirect('consultation:ordonnance_list')

        return render(request, self.template_name, {
            'ordonnance_form': ordonnance_form,
            'formset': formset
        })


class OrdonnanceListView(ListView):
    model = Ordonnance
    template_name = 'interface_docteur/ordonnances/ordonnance_list.html'
    context_object_name = 'ordonnances'
    ordering = ['-date']
    
    
class OrdonnanceDetailView(DetailView):
    model = Ordonnance
    template_name = 'interface_docteur/ordonnances/ordonnance_detail.html'
    context_object_name = 'ordonnance'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['traitements'] = self.object.traitements.filter(deleted_at__isnull=True)
        return context
    
    
class OrdonnanceUpdateView(View):
    template_name = 'interface_docteur/ordonnances/ordonnance_form.html'

    def get(self, request, pk):
        ordonnance = get_object_or_404(Ordonnance, pk=pk)
        ordonnance_form = OrdonnanceForm(instance=ordonnance)
        formset = TraitementFormSet(instance=ordonnance, prefix='traitement')
        return render(request, self.template_name, {
            'ordonnance_form': ordonnance_form,
            'formset': formset,
            'ordonnance': ordonnance
        })

    def post(self, request, pk):
        ordonnance = get_object_or_404(Ordonnance, pk=pk)
        ordonnance_form = OrdonnanceForm(request.POST, instance=ordonnance)
        formset = TraitementFormSet(request.POST, instance=ordonnance, prefix='traitement')

        if ordonnance_form.is_valid() and formset.is_valid():
            ordonnance = ordonnance_form.save()
            traitements = formset.save(commit=False)

            # On les associe manuellement à l'ordonnance
            for traitement in traitements:
                traitement.ordonnance = ordonnance
                traitement.save()

            # Suppression des traitements marqués pour suppression (si tu le gères)
            for obj in formset.deleted_objects:
                obj.delete()

            formset.save_m2m()

            return redirect('consultation:ordonnance_detail', pk=ordonnance.pk)

        return render(request, self.template_name, {
            'ordonnance_form': ordonnance_form,
            'formset': formset,
            'ordonnance': ordonnance
        })

class OrdonnanceDeleteView(DeleteView):
    model = Ordonnance
    template_name = 'ordonnances/ordonnance_confirm_delete.html'
    success_url = reverse_lazy('ordonnance_list')