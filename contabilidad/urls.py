from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'conta'

urlpatterns = [
    path('',views.lista_transacciones,name="transaccion-lista"),
    path('catalogo/',views.ListarCatalogo,name="catalogo"),
    path('cargaBalance/',views.CargarBalance,name="cargar-balance"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
