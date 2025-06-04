from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home

urlpatterns = [ 
    path('',home,name='home'),
    path('accounts/', include('personnels.urls')),
    path('conixgest/', admin.site.urls),
    path('pharmacie/',include('pharmacie.urls', namespace='pharmacie')),
    path('pharmacieGarde/',include('pharmacie_garde.urls', namespace='pharmacie_garde')),
    path('caisse/',include('caisse.urls', namespace='caisse')),
    path('caisse/garde/',include('caisse_garde.urls', namespace='caisse_garde')),
    path('patient/',include('patients.urls', namespace='patient')),
    path('pansement/',include('pansement.urls', namespace='pansement')),
    path('viol/',include('viol.urls', namespace='Viol')),
    path('vaccin/',include('vaccin.urls', namespace='vaccin')),
    path('laboratoire/',include('laboratoire.urls', namespace='laboratoire')),
    path('hospitalisation/',include('hospitalisation.urls', namespace='hospitalisation')),
    path('echographie/',include('echographie.urls', namespace='echographie')),
    path('consultation/',include('consultation.urls', namespace='consultation')),
    path('blocoperatoire/',include('blocoperatoire.urls', namespace='blocoperatoire')),
    path('mto/',include('mto.urls', namespace='mto')),
    path('rendez_vous/',include('rendez_vous.urls', namespace='rendez_vous')),
    path('csiMakelekele/', include('csi_makelekele.urls',namespace='prestation')),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

