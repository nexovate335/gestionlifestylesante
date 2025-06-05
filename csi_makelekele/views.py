from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView, View
)
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from .models import Prestation
from .forms import PrestationForm
from collections import Counter
from django.db.models import Count
from django.utils.timezone import now
from datetime import datetime
from django.utils.timezone import make_aware, get_current_timezone, now
from datetime import datetime, time, timedelta


# Liste des prestations
class PrestationListView(ListView):
    model = Prestation
    template_name = "csi_makelekele/prestations/prestation_list.html"
    context_object_name = "prestations"

    def get_queryset(self):
        queryset = Prestation.objects.all().order_by('-date')

        # Filtrer par type
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)

        # Filtrer par date avec intervalle datetime aware
        date_filter = self.request.GET.get('date')
        if date_filter:
            try:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                tz = get_current_timezone()
                start_datetime = make_aware(datetime.combine(date_obj, time.min), timezone=tz)
                next_day = date_obj + timedelta(days=1)
                end_datetime = make_aware(datetime.combine(next_day, time.min), timezone=tz)
                queryset = queryset.filter(date__gte=start_datetime, date__lt=end_datetime)
            except ValueError:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = (
            Prestation.objects.values_list("type", flat=True)
            .distinct()
            .order_by("type")
        )
        context["type_counts"] = dict(
            Prestation.objects.values("type")
            .annotate(count=Count("type"))
            .values_list("type", "count")
        )
        # Date au format ISO pour input type=date
        context["today"] = now().date().isoformat()

        # Dates aware pour filtre dans le template "Voir les prestations d’aujourd’hui"
        tz = get_current_timezone()
        today_date = now().date()
        start_datetime = make_aware(datetime.combine(today_date, time.min), timezone=tz)
        next_day = today_date + timedelta(days=1)
        end_datetime = make_aware(datetime.combine(next_day, time.min), timezone=tz)
        context["filter_start_date"] = start_datetime.isoformat()
        context["filter_end_date"] = end_datetime.isoformat()

        return context

# Création d'une prestation
class PrestationCreateView(CreateView):
    model = Prestation
    form_class = PrestationForm
    template_name = "csi_makelekele/prestations/prestation_form.html"
    success_url = reverse_lazy("prestation:prestation_list")

    
# Détails d'une prestation
class PrestationDetailView(DetailView):
    model = Prestation
    template_name = "csi_makelekele/prestations/prestation_detail.html"
    context_object_name = "prestation"


# Mise à jour d'une prestation
class PrestationUpdateView(UpdateView):
    model = Prestation
    form_class = PrestationForm
    template_name = "csi_makelekele/prestations/prestation_form.html"  # tu peux utiliser le même que create
    success_url = reverse_lazy("prestation:prestation_list")



# Suppression logique d'une prestation
class PrestationDeleteView(View):
    def post(self, request, *args, **kwargs):
        prestation = get_object_or_404(Prestation.objects, pk=self.kwargs["pk"])
        prestation.deleted_at = now()
        prestation.save()
        return redirect(reverse_lazy("prestation:prestation_list"))


# Restauration d'une prestation supprimée
class PrestationRestoreView(View):
    def post(self, request, pk):
        prestation = get_object_or_404(Prestation.all_objects.filter(deleted_at__isnull=False), pk=pk)
        prestation.restore()
        return redirect(reverse_lazy("prestation:prestation_deleted_list"))


# Liste des prestations supprimées
class PrestationDeletedListView(ListView):
    model = Prestation
    template_name = "csi_makelekele/prestations/prestation_deleted_list.html"
    context_object_name = "prestations_deleted"

    def get_queryset(self):
        return Prestation.all_objects.filter(deleted_at__isnull=False)
