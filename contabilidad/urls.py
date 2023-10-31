from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'conta'

urlpatterns = [
    path('',views.cargarBalanceGeneral,name="transaccion-lista"),
    path('catalogo/',views.ListarCatalogo,name="catalogo"),
    path('cargaEmpresa/',views.CrearEmpresa,name="cargar-balance"),
    path('estado_resultados/', login_required(views.VerEstadoResultado.as_view()), name="ver_estado_resultado"),
    path('graficoVaricacion/', views.grafico_var, name='variacion_cuenta'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
