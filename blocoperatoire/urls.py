from django.urls import path
from .views import *

app_name = 'blocoperatoire'

urlpatterns = [
    path('blocoperatoire', BlocOperatoireRecepListView.as_view(), name='blocoperatoire_list_recep'),
    path('', BlocOperatoireListView.as_view(), name='blocoperatoire_list'),
    path('create/', BlocOperatoireCreateView.as_view(), name='blocoperatoire_create'),
    path('<int:pk>/', BlocOperatoireDetailView.as_view(), name='blocoperatoire_detail'),
    path('<int:pk>/update/', BlocOperatoireUpdateView.as_view(), name='blocoperatoire_update'),
    path('<int:pk>/bloc/', BlocOperatoireUserUpdateView.as_view(), name='blocoperatoire_update_user'),
    path('<int:pk>/delete/', BlocOperatoireDeleteView.as_view(), name='blocoperatoire_delete'),
    path('<int:pk>/restore/', BlocOperatoireRestoreView.as_view(), name='blocoperatoire_restore'),
    path('deleted/', BlocOperatoireDeletedListView.as_view(), name='blocoperatoire_deleted_list'),
]
