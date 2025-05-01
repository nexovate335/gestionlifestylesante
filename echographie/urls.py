from django.urls import path
from .views import (
    EchographieListView, EchographieCreateView, EchographieDetailView,
    EchographieUpdateView, EchographieDeleteView, EchographieRestoreView,
    EchographieDeletedListView
)

app_name = "echographie"

urlpatterns = [
    path("", EchographieListView.as_view(), name="echographie_list"),
    path("create/", EchographieCreateView.as_view(), name="echographie_create"),
    path("<int:pk>/", EchographieDetailView.as_view(), name="echographie_detail"),
    path("<int:pk>/update/", EchographieUpdateView.as_view(), name="echographie_update"),
    path("<int:pk>/delete/", EchographieDeleteView.as_view(), name="echographie_delete"),
    path("deleted/", EchographieDeletedListView.as_view(), name="echographie_deleted_list"),
    path("<int:pk>/restore/", EchographieRestoreView.as_view(), name="echographie_restore"),
]
