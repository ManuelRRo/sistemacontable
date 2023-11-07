from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'conta'

urlpatterns = [
    path('',views.home,name="home"),
    path('estados_financieros/',views.estados_financieros,name="ver_estados_financieros"),
    path('balance_general',views.VerBalanceGeneral.as_view(),name="ver_balance_general"),
    path('balance/actualizar-monto/<int:id_cuenta>',views.TransaccionUpdateView.as_view(),name="actualizar-monto"),
    path('catalogo/',views.ListarCatalogo,name="catalogo"),
    path('cargaEmpresa/',views.CrearEmpresa,name="cargar-balance"),
    path('estado_resultados/', login_required(views.VerEstadoResultado.as_view()), name="ver_estado_resultado"),
    path('graficoVaricacion/', views.grafico_var, name='variacion_cuenta'),
    path('ratios_analisis_horizontal/',views.calcular_ratios2,name="calcular_ratios"),
    #HU-05-Definir Cuentas Ratios
    path('homeRatios/',views.homeRatios,name="home-ratios"),
    path('selectRatios/',views.ActualizarCuentasRatios,name="crear-cuentas-ratios"),
    path('comparacion_ratios_empresas_promedio/',views.comparacionRatiosEmpresasPromedio,name="comparacion-ratios-empresas-promedios"),
    path('grafico_ratios/',views.graficoRatios,name="grafico_ratios"),
    # Benchmark
    path('benchmark/', login_required(views.Benchmark.as_view()), name="ver_benchmark"),
    path('comparacion_ratios_empresas_valor/',views.comparacionRatiosEmpresasValor,name="comparacion-ratios-empresas-valor"),
    #HU-006-Analisis Vertical
    path('analisis_vertical/',views.analisisVertical,name="analisis_vertical"),
    #HU-007-Analisis Horizontal
    path('analisis_horizontal/',views.analisisHorizontal,name="analisis_horizontal"),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
