from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'conta'

urlpatterns = [
    path('',views.cargarBalanceGeneral,name="transaccion-lista"),
    path('balance/actualizar-monto/<int:id_cuenta>',views.TransaccionUpdateView.as_view(),name="actualizar-monto"),
    path('catalogo/',views.ListarCatalogo,name="catalogo"),
    path('cargaEmpresa/',views.CrearEmpresa,name="cargar-balance"),
    path('estado_resultados/', login_required(views.VerEstadoResultado.as_view()), name="ver_estado_resultado"),
    path('graficoVaricacion/', views.grafico_var, name='variacion_cuenta'),
    path('calcular_ratios/',views.calcular_ratios,name="calcular_ratios"),
    #HU-05-Definir Cuentas Ratios
    path('homeRatios/',views.homeRatios,name="home-ratios"),
    path('selectRatios/',views.ActualizarCuentasRatios,name="crear-cuentas-ratios"),
    path('comparacion_ratios_empresas/',views.comparacionRatiosEmpresas,name="comparacion-ratios-empresas"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
