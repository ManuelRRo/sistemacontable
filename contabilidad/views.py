from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.views.generic import View
from django.db.models import Q
from django.contrib import messages
import pandas
from django.db.models import Sum
from decimal import Decimal
from .forms import CatalagoForm,EmpresaForm,ActivoCorrienteForm,UpdateTransaccionForm
from .models import Catalogo, Transaccion,Cuenta,Propietario,Empresa,Ratio
from datetime import datetime,date
import matplotlib
matplotlib.use('Agg')
import plotly.express as px
import pandas as pd
import os
from asgiref.sync import sync_to_async
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from plotly.io import to_image
from io import BytesIO
import base64
import json


#HU-002-Registrar empresa con catálogo, BGN Y ERS en formato excel
def CrearEmpresa(request):

    contexto = {}
    
    try:
        propietario_empresa = request.user.propietario
    except:
        print("No tiene Propietario Asignado")
        contexto = {}
        contexto["propietario"] = False
        return render(request,'empresa/crear-empresa.html',contexto)

    if request.method == 'POST':

        form = CatalagoForm(request.POST,
                            request.FILES)
        empresa_form = EmpresaForm(request.POST)
        print(form.errors)
        if form.is_valid() and empresa_form.is_valid():
            #Crear catalogo
            catalogo_excel = form.save()
            #get nombre empresa
            nombreempresa = empresa_form.cleaned_data['nombre_empresa']
            sectorempresa = empresa_form.cleaned_data['sectores']
            #Crear la empresa
            new_empresa = Empresa(nombre_empresa=nombreempresa,
                                  sector=sectorempresa,
                                  catalogo_empresa=catalogo_excel,
                                  propietario=propietario_empresa)
            new_empresa.save()
            #activar la empresa
            p = Propietario.objects.get(user=request.user)
            p.empresactiva = True
            p.save()
            
            #Leer catalogo en excel
            path = f"{settings.MEDIA_ROOT}/{catalogo_excel.archivo}"
            hoja_bgn = pandas.read_excel(path,sheet_name="BGN")
            balance = {}

            #Crear Cuentas de Ratios
            for ratio in Ratio.NombreRatio.choices:
                print(ratio)

            lista_anios = [hoja_bgn.columns[2], hoja_bgn.columns[3], hoja_bgn.columns[4]]
            
            for index, row in hoja_bgn.iterrows():
                #Extraer primer caracter de la columna codigo
                cod = str(row['codigo'])[0]
                tipo = ''
                #Asginar categoria de acuerdo al primer caracter del codigo del catalago
                if cod == '1':
                    tipo = Cuenta.Categoria.ACTIVO
                if cod == '2':
                    tipo = Cuenta.Categoria.PASIVO
                if cod == '3':
                    tipo = Cuenta.Categoria.PATRIMONIO
                #Agregar una opcion para generar el catalogo primero
                # y luego solo pasarlo aqui para agrupar las cuentas por catalogo
                cuenta = Cuenta.objects.create(
                    codigo = row["codigo"],
                    nombre = row["cuenta"],
                    categoria = tipo,
                    catalogo = catalogo_excel
                )
                try:
                    for anio in lista_anios:
                        t = Transaccion.objects.create(
                            monto=Decimal(row[anio]),
                            descripcion="Cuenta del " + str(anio),
                            slug="Balance general",
                            cuenta=cuenta,
                            fecha_creacion=f"{str(anio)}-10-25 00:00:00",
                            tipo_transaccion="CMP",
                            naturaleza = "DBT"
                        )
                except:
                    print(row[anio])

            # Leer hoja ERS - Estado de Resultados
            hoja_ers = pandas.read_excel(path, sheet_name="ERS")

            # Obtener años
            lista_anios = [hoja_ers.columns[2], hoja_ers.columns[3], hoja_ers.columns[4]]

            # Variables a utilizar
            codigo_ers = ''
            categoria_ers = ''
            subcategoria_ers = ''
            naturaleza_ers = ''

            for index, row in hoja_ers.iterrows():
                # Extraer caracteres de la columna codigo
                codigo_ers = str(row['codigo'])
                categoria_ers = ''

                # Asignar categoria de cada cuenta
                if codigo_ers[0] == '4':
                    categoria_ers = Cuenta.Categoria.RESULTADOS_DEUDORAS
                    naturaleza_ers = Transaccion.Naturaleza.CREDITO
                    # Asignar subcategoria
                    if codigo_ers[1] == '1':
                        subcategoria_ers = Cuenta.Subcategoria.COSTOS
                    elif codigo_ers[1] == '2':
                        subcategoria_ers = Cuenta.Subcategoria.GASTOS_OPERACIONALES
                elif codigo_ers[0] == '5':
                    categoria_ers = Cuenta.Categoria.RESULTADOS_ACREEDORAS
                    naturaleza_ers = Transaccion.Naturaleza.DEBITO
                    # Asignar subcategoria
                    if codigo_ers[1] == '1': 
                        subcategoria_ers = Cuenta.Subcategoria.INGRESOS_OPERACIONALES
                else:
                    categoria_ers = Cuenta.Categoria.ESTADO_RESULTADOS
                    subcategoria_ers = Cuenta.Subcategoria.NINGUNA
                
                # Crear cuenta con los datos anteriores
                cuenta_ers = Cuenta.objects.create(
                    codigo = row["codigo"],
                    nombre = row["cuenta"],
                    categoria = categoria_ers,
                    subcategoria = subcategoria_ers,
                    catalogo = catalogo_excel
                )

                for anio in lista_anios:
                    Transaccion.objects.create(
                        monto=Decimal(row[anio]),
                        descripcion="Cuenta del " + str(anio),
                        slug="Estado de Resultado",
                        cuenta=cuenta_ers,
                        fecha_creacion=f"{str(anio)}-12-31 00:00:00",
                        tipo_transaccion="OPE",
                        naturaleza = naturaleza_ers
                    )


            contexto["balance"] = "Balance general cargado correctamente"
            return redirect('conta:transaccion-lista')
    else:
        form = CatalagoForm()
        empresa_form = EmpresaForm()
        contexto["form"]=form
        contexto["empresa_form"] = empresa_form 
        contexto["propietario"] = True

    return render(request,'empresa/crear-empresa.html',contexto)
#HU HOME RATIOS
def homeRatios(request):
    return render(request,'ratios/homeRatios.html')

#HU-005 Definir Cuentas de Ratios
def actualizarCuentaRatio(primary_key,codigo_ratio):
    objeto = Cuenta.objects.get(pk=primary_key)
    objeto.cuenta_ratio = codigo_ratio
    return objeto

def ActualizarCuentasRatios(request):
    context = {}
    lista = []
    codigo_ratios = Cuenta.CuentaRatio.values[1:]
    cuenta_= request.POST 
    id_ratios_vistos = set()
    #print(request.POST)

    if request.method == 'POST':
        if len(cuenta_) != 0 :
            for nombre_ratio, id_ratio in cuenta_.items():
                # Ignorar el csrfmiddlewaretoken
                if nombre_ratio != 'csrfmiddlewaretoken':
                    # Verificar si el ID de ratio ya fue visto
                    if id_ratio in id_ratios_vistos:
                        context["form_as"] = ActivoCorrienteForm(request_=request,user=None)
                        context["error_message"] = "Seleccione una cuenta diferente para cada Ratio"
                        #print("Formulario en contexto:", context.get("form_as"))
                        return render(request,'ratios/HU-005-cuenta-ratios.html',context)
                    else:
                        # Agregar el ID de ratio al conjunto
                        id_ratios_vistos.add(id_ratio)
                
            for cuenta, codigo_ratio in zip(cuenta_, codigo_ratios):
                if cuenta != "csrfmiddlewaretoken":
                            actualizarCuentaRatio(request.POST.get(cuenta),codigo_ratio).save()
                        
    
    context["form_as"] = ActivoCorrienteForm(request_=request,user=request.user)
    context["error_message"] = None
    #Crear Cuentas de Ratios
    return render(request,'ratios/HU-005-cuenta-ratios.html',context)
#HU-19-Grafico de variacion

def grafico_var(request):
    try:
        user = request.user
        propietario = Propietario.objects.get(user=user)
        empresa = Empresa.objects.get(propietario=propietario)
        cuentas_balance = Cuenta.objects.filter(categoria__in=['ASV', 'PSV', 'PTR'], catalogo=empresa.catalogo_empresa)
        
        if request.method == "POST":
            fecha_inicio = request.POST['fechainicio']
            fecha_final = request.POST['fechafinal']
            año_inicio, mes_inicio, dia_inicio = map(int, fecha_inicio.split('-'))
            año_final, mes_final, dia_final = map(int, fecha_final.split('-'))
            
            seleccionada = request.POST['cuenta']
            cuenta = Cuenta.objects.get(id=seleccionada)
        

            saldos = []
            for año in range(año_inicio, año_final + 1):
                fecha_in = date(año, mes_inicio, dia_inicio)
                fecha_end = date(año, mes_final, dia_final)
                saldo = Transaccion.objects.filter(cuenta=seleccionada, fecha_creacion__range=[fecha_in, fecha_end]).aggregate(Sum('monto'))
                saldos.append((año, saldo))
                
            años = [año for año, _ in saldos]
            saldos = [saldo['monto__sum'] for _, saldo in saldos]
            
            fig = px.line(pd.DataFrame({'Año': años, 'Saldo': saldos}), x="Año", y="Saldo", title=f"Cuenta de <b>{cuenta.nombre}</b>, período <b>{año_inicio} - {año_final}</b>")
            fig.update_layout(width=1000, height=600)
            
            años_con_saldos = [año for año, saldo in zip(años, saldos) if saldo is not None]
            fig.add_trace(go.Scatter(x=años_con_saldos, y=[saldos[años.index(año)] for año in años_con_saldos], mode='markers', marker=dict(size=10, color='red'), name='valores'))
            fig.update_xaxes(tickmode='array', tickvals=años, ticktext=[str(año) for año in range(año_inicio, año_final + 1)])
            grafico_var = fig.to_html(full_html=False, include_plotlyjs='cdn')
            mostrarGrafico = True
        else:
            mostrarGrafico = False
            grafico_var = None
    except Exception as e:
        messages.error(request, f'Error al generar el gráfico')
        return render(request, 'graficos/variacion_cuenta.html', {'cuentas_balance': cuentas_balance})
    
    return render(request, 'graficos/variacion_cuenta.html', {'cuentas_balance': cuentas_balance, 'mostrarGrafico': mostrarGrafico, 'grafico_var': grafico_var})
@sync_to_async
def graficoRatios(request):
    try:
        mostrarGrafico = False
        figs = []
        usuario = request.user
        try:
            propietarioemprsa = get_object_or_404(Propietario, user=usuario)
        except:
            messages.error(request, "No hay propietario registrado")
            return render(request, 'graficos/ratios.html', {'ratios': ratios})
        try:
            emprsa = get_object_or_404(Empresa, propietario=propietarioemprsa)
        except:
            messages.error(request, "No hay empresa registrada")
            return render(request, 'graficos/ratios.html', {'ratios': ratios})
        anio = 2023
        ratios = funcionRatios(anio, request, emprsa)
        data = []
        anios = []
        if request.method == 'POST':
            mostrarGrafico = True
            ratios_seleccionados = request.POST.getlist("ratios")
            fecha_inicio = request.POST.get("fechainicio")
            fecha_final = request.POST.get("fechafinal")
            try:
                año_inicio, mes_inicio, dia_inicio = map(int, fecha_inicio.split('-'))
                año_final, mes_final, dia_final = map(int, fecha_final.split('-'))
            except:
                messages.error(request, "Seleccione fechas válidas")
                return render(request, 'graficos/ratios.html', {'ratios': ratios})
            if len(ratios_seleccionados) < 5:
                messages.error(request, "Se deben seleccionar al menos 5 ratios")
                return render(request, 'graficos/ratios.html', {'ratios': ratios})
            if año_final - año_inicio < 2:
                messages.error(request, "El rango de fechas debe ser de al menos 3 año")
                return render(request, 'graficos/ratios.html', {'ratios': ratios})   
            for anio in range(año_inicio, año_final + 1):
                ratios = funcionRatios(anio, request, emprsa)
                data.append({"anio": anio, "ratios": ratios})
                anios.append(anio)
            for i, ratio in enumerate(data[0]['ratios']):
                if(ratio['nombre'] not in ratios_seleccionados):
                    continue
                ratio_nombre = ratio['nombre']
                fig, ax = plt.subplots()
                anios_data = [anio_data['anio'] for anio_data in data]
                valores = [float(anio_data['ratios'][i]['valor']) for anio_data in data]
                for anio, valor in zip(anios_data, valores):
                    ax.annotate(f'{valor:.2f}', (anio, valor), textcoords="offset points", xytext=(5, 10), ha='center')
                for anio_data in data:
                    anio = anio_data['anio']
                    valor = float(anio_data['ratios'][i]['valor'])
                    ax.plot(anio,valor,marker='o', label=str(anio))
                ax.plot([anio_data['anio'] for anio_data in data], [float(anio_data['ratios'][i]['valor']) for anio_data in data],color='black', linestyle='-')
                ax.set_xlabel('Año')
                ax.set_ylabel('Valor')
                ax.set_title('Ratio De '+ ratio_nombre +' Periodo ' + str(año_inicio) + ' - ' + str(año_final))
                ax.legend()
                ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                image_base64 = base64.b64encode(buffer.read()).decode()
                plt.close() 
                figs.append({'nombre': ratio_nombre, 'imagen_base64': f"data:image/png;base64,{image_base64}"})
            return render(request, 'graficos/ratios.html', {'ratios': ratios, 'graficos': figs, 'mostrarGrafico': mostrarGrafico})
    except:
        messages.error(request, "Error al generar los gráficos, Verifique haber definido las cuentas para los ratios, y que existan saldos en el periodo seleccionado")
        return render(request, 'graficos/ratios.html', {'ratios': ratios})

    return render(request, 'graficos/ratios.html', {'ratios': ratios})
#HU-023-Listar Cuentas del Catalogo
def ListarCatalogo(request):
    catalogo = {}
    try:
        catalogo = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
    except:
        print("No hay catalogo")
    return render(request,'catalogo/listar-catalogo.html',{'catalogo':catalogo})

#HU-24-Listar balance general
@login_required()
def cargarBalanceGeneral(request):
    usuario = request.user
    try:
        propietarioemprsa = get_object_or_404(Propietario,user=usuario)

    except:
        print("No hay propietario")

    try:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
        
    except Exception as e:
        error_message = f"Se produjo una excepción: {str(e)}"
        print(error_message)
        print("No tiene empresa registrada")
        
    contexto = {}    
    totalactivos = 0
    total = 0
    year_1 = ""
    year_2 = ""
    lista_trans = Transaccion.objects.all()
   
    diccionario_cuentas = {}
    #Sumar montos #Debo crear un diccionario con la cuenta y monto que tiene
    if request.method == "POST":
        year_1 = request.POST['fechainicio']# retorna como anio-mes-dia
        year_2 = request.POST['fechafinal']# retorna como anio-mes-dia
    else:
        year_1 = timezone.now().strftime('%Y-%m-%d')
        year_2 = timezone.now().strftime('%Y-%m-%d')

    try:
        contexto = sumarTransacciones(request)
        print("contexto_)sumas",contexto)
    except Exception as e:
        error_message = f"Se produjo una excepción: {str(e)}"
        print(error_message)
        print("Problema en sumarTrasnsacciones")
    
    year_1 = timezone.now().year
    year_2 = timezone.now().year
    try:
        contexto = sumarTransacciones(request,op=0)
    except Exception as e:
        error_message = f"Se produjo una excepción: {str(e)}"
        print(error_message)
    return render(request,
           'balance/listar-balance.html'
           ,contexto)

def sumarTransacciones(request,year_1=None,year_2=None,op=1):
    cuentasActivos = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
    diccionario_cuentas = {}
    contexto = {}
    totalactivos = 0
    total = 0
    anio_1 = ""
    anio_2 = ""
    if op == 1:
        anio_1 = year_1
        anio_2 = year_2
    else:
        #date(anio,mes,dia)
        anio_1 = date(timezone.now().year,1,1)
        anio_2 = date(timezone.now().year,12,31)

    for cuenta in cuentasActivos:
        saldoCredito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.CREDITO,
                                                    fecha_creacion__range=(anio_1,anio_2)
                                                ).aggregate(total=Sum('monto'))
        saldoDebito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.DEBITO,
                                                    fecha_creacion__range=(anio_1,anio_2)
                                                ).aggregate(total=Sum('monto'))
        try:
            id_trans = cuenta.transacciones.get(naturaleza=Transaccion.Naturaleza.DEBITO,fecha_creacion__range=(anio_1,anio_2))
            print(id_trans)
        except Exception as e:
            error_message = f"Se produjo una excepción: {str(e)}"
            print("saldo debito pk",type(id_trans))

        if saldoCredito["total"] is None:
            saldoCredito["total"] = Decimal(0.0)
        if saldoDebito["total"] is None:
            saldoDebito["total"] = Decimal(0.0)
        total = saldoDebito["total"] - saldoCredito["total"]
        totalactivos += total 

        

        diccionario_cuentas[cuenta] = {
        'saldo_credito': saldoCredito["total"],
        'saldo_debito': saldoDebito["total"],
        'total': total,
        'num_cuenta': id_trans.pk
        }


    contexto = {'cuentasActivos': cuentasActivos,
        'totalActivos': total,
        'diccionario_cuentas':diccionario_cuentas,
        'pathbase':settings.BASE_DIR,}
        
    return contexto

class TransaccionUpdateView(UpdateView):
    model = Transaccion
    form_class = UpdateTransaccionForm
    template_name = 'balance/transaccion_update.html'
    success_url = reverse_lazy('conta:transaccion-lista')

    def get_object(self, queryset=None):
        # Obtener el objeto que se va a actualizar
        objeto = Transaccion.objects.get(pk=self.kwargs['id_cuenta'])
        return objeto
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["nombre_cuenta"] = obj.cuenta
        return context
#HU-25-Listar Estados de Resultado
# Mostrar Estados de Resultados 
# (Empresa Registrada)
# Se ha implementado el login_required
class VerEstadoResultado(View):
    model_transaccion = Transaccion
    model_empresa = Empresa
    template_name = 'estados_financieros/estado_resultados.html'

    def get_queryset(self):
        context = {}
        empresa = self.model_empresa.objects.get(propietario__user=self.request.user)
        # Crear tres objetos Q, uno para cada categoría
        q1 = Q(cuenta__categoria=Cuenta.Categoria.RESULTADOS_DEUDORAS)
        q2 = Q(cuenta__categoria=Cuenta.Categoria.RESULTADOS_ACREEDORAS)
        q3 = Q(cuenta__categoria=Cuenta.Categoria.ESTADO_RESULTADOS)
        q4 = Q(cuenta__catalogo=empresa.catalogo_empresa)
        # Combinar los objetos Q con el operador 'OR' usando '|'
        context["transaccion_cuenta"] = self.model_transaccion.objects.filter((q1 | q2 | q3) & q4)
        context["empresa"] = empresa
        return context
    
    def get_context_data(self, **kwargs):
        context = {}
        context.update(self.get_queryset()) 
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        context = {}
        fecha_inicio = request.POST['fechainicio']
        fecha_final = request.POST['fechafinal']
        # Convierte las fechas a objetos de tipo datetime
        fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_final_obj = datetime.strptime(fecha_final, '%Y-%m-%d')
        # Obtiene el rango de años entre las fechas de inicio y final
        rango_de_anios = [str(anio) for anio in range(fecha_inicio_obj.year, fecha_final_obj.year + 1)]
        # Generando diccionario para template estado_resultados.html
        transaccion_cuenta = self.get_context_data()["transaccion_cuenta"].filter(fecha_creacion__range=(fecha_inicio,fecha_final))
        
       # Crear un diccionario para almacenar transacciones por año
        transacciones_por_anio = {}

        for anio in rango_de_anios:
            transacciones_por_anio[anio] = []

        for transaccion in transaccion_cuenta:
            anio_transaccion = str(transaccion.fecha_creacion.year)
            if anio_transaccion in transacciones_por_anio:
                transacciones_por_anio[anio_transaccion].append(transaccion)

        context["transacciones_por_anio"] = transacciones_por_anio
        context["empresa"] = self.get_context_data()["empresa"]
        context["fecha_inicio"] = fecha_inicio
        context["fecha_final"] = fecha_final
        context["rango_de_anios"] = rango_de_anios
        context["cuentas"] = transacciones_por_anio[rango_de_anios[0]]
        

        return render(request, self.template_name, context) 
def funcionRatios(anio,request,emprsa):
    propietarioemprsa = get_object_or_404(Propietario,user=request.user)
    if emprsa is None:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
    activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    pasivoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="PSVC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    inventario=Transaccion.objects.filter(cuenta__cuenta_ratio="INVT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    activosTotales=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTV", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    efectivo=Transaccion.objects.filter(cuenta__cuenta_ratio="EFCT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    valoresCortoPlazo=Transaccion.objects.filter(cuenta__cuenta_ratio="VLRS", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    costoDeVenta=Transaccion.objects.filter(cuenta__cuenta_ratio="CSTDV", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    ventasNetas=Transaccion.objects.filter(cuenta__cuenta_ratio="VNTSN", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    cuentasPorPagarComerciales=Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPP", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    cuentasPorCobrarComerciales=Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto    
    cuentasPorCobrarComercialesAnterior=Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio-1).first()  
    cuentasPorPagarComercialesAnterior=Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPP", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio-1).first()   
    inventarioAnterior=Transaccion.objects.filter(cuenta__cuenta_ratio="INVT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio-1).first()
    compras=Transaccion.objects.filter(cuenta__cuenta_ratio="CSTDV", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    
    razonCirculante=activoCorriente/pasivoCorriente
    pruebaAcida=(activoCorriente-inventario)/pasivoCorriente
    razonCapitalTrabajo=(activoCorriente-pasivoCorriente)/activosTotales
    razonEfectivo=(efectivo+valoresCortoPlazo)/pasivoCorriente
    if inventarioAnterior:
        razonRotacionInventario=costoDeVenta/((inventario+inventarioAnterior.monto)/2)
        razonDiasInventario=((inventario+inventarioAnterior.monto)/2)/(costoDeVenta/365)
    else:
        razonRotacionInventario=costoDeVenta/inventario
        razonDiasInventario=inventario/(costoDeVenta/365)
    if cuentasPorCobrarComercialesAnterior:
        razonRotacionCuentasPorCobrar=ventasNetas/((cuentasPorCobrarComerciales+cuentasPorCobrarComercialesAnterior.monto)/2)
        razonPeriodoMedioCobranza=(((cuentasPorCobrarComerciales+cuentasPorCobrarComercialesAnterior.monto)/2)*365)/ventasNetas
    else:
        razonRotacionCuentasPorCobrar=ventasNetas/cuentasPorCobrarComerciales
        razonPeriodoMedioCobranza=(cuentasPorCobrarComerciales*365)/ventasNetas
    if cuentasPorPagarComercialesAnterior:
        razonRotacionCuentasPorPagar=compras/((cuentasPorPagarComerciales+cuentasPorPagarComercialesAnterior.monto)/2)
        periodoMedioPago=(((cuentasPorPagarComerciales+cuentasPorPagarComercialesAnterior.monto)/2)*365)/compras
    else:
        razonRotacionCuentasPorPagar=compras/cuentasPorPagarComerciales
        periodoMedioPago=(cuentasPorPagarComerciales*365)/compras

    ratios=[
        {"nombre":"Razón circulante","valor":razonCirculante},
        {"nombre":"Prueba ácida","valor":pruebaAcida},
        {"nombre":"Razón de capital de trabajo","valor":razonCapitalTrabajo},
        {"nombre":"Razón de efectivo","valor":razonEfectivo},
        {"nombre":"Razón de rotación de inventario","valor":razonRotacionInventario},
        {"nombre":"Razón de días de inventario","valor":razonDiasInventario},
        {"nombre":"Razón de rotación de cuentas por cobrar","valor":razonRotacionCuentasPorCobrar},
        {"nombre":"Razón de período medio de cobranza","valor":razonPeriodoMedioCobranza},
        {"nombre":"Razón de rotación de cuentas por pagar","valor":razonRotacionCuentasPorPagar},
        {"nombre":"Período medio de pago","valor":periodoMedioPago}
    ]
    return ratios

def calcular_ratios(request):
    try:
        propietarioemprsa = get_object_or_404(Propietario,user=request.user)

    except:
        print("No hay propietario")

    try:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
        
    except:
        print("No tiene empresa registrada")
    
    anio=2023
    activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first()
    
    if activoCorriente is None:
        ratios=[]
    else:
        ratios=funcionRatios(anio,request,None)
            
    #Sumar montos #Debo crear un diccionario con la cuenta y monto que tiene
    if request.method == "POST":
        year_1 = request.POST['fechainicio']# retorna como anio-mes-dia
        year_2 = request.POST['fechafinal']# retorna como anio-mes-dia
    else:
        year_1 = timezone.now().strftime('%Y-%m-%d')
        year_2 = timezone.now().strftime('%Y-%m-%d')  
    return render(request,"ratios/calcular-ratios.html",{'ratios':ratios,'empresa':emprsa})

def comparacionRatiosEmpresasPromedio(request):
    if request.method=="POST":
        activosTotales=Transaccion.objects.filter()
    try:
        propietarioemprsa = get_object_or_404(Propietario,user=request.user)

    except:
        print("No hay propietario")

    try:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
        
    except:
        print("No tiene empresa registrada")

    anio=2023
    activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first()
    empresa1 = get_object_or_404(Empresa,propietario=propietarioemprsa)
    empresa2 = get_object_or_404(Empresa,id=8)
    empresas=[
        {"nombre":empresa1},
        {"nombre":empresa2}
    ]
    ratios1=[]
    ratios2=[]
    if activoCorriente is None:
        ratios1=[]
        ratios2=[]
    else:
        
        ratios1=funcionRatios(anio,request,empresa1)
        ratios2=funcionRatios(anio,request,empresa2)
    
    promedios=[
        {"nombre":"Razón circulante"},
        {"nombre":"Prueba ácida"},
        {"nombre":"Razón de capital de trabajo"},
        {"nombre":"Razón de efectivo"},
        {"nombre":"Razón de rotación de inventario"},
        {"nombre":"Razón de días de inventario"},
        {"nombre":"Razón de rotación de cuentas por cobrar"},
        {"nombre":"Razón de período medio de cobranza"},
        {"nombre":"Razón de rotación de cuentas por pagar"},
        {"nombre":"Período medio de pago"}
    ]
    for elemento,ratio1, ratio2 in zip(promedios,ratios1, ratios2):
        promedio=(ratio1['valor'] + ratio2['valor']) / 2

        elemento['ratio1']=ratio1['valor']
        elemento['ratio2']= ratio2['valor']
        elemento['promedio']=promedio
    
        if ratio1['valor']>=promedio:
            elemento['ratio1esMayor']=True
        else:
            elemento['ratio1esMayor']=False

        if ratio2['valor']>=promedio:
            elemento['ratio2esMayor']=True
        else:
            elemento['ratio2esMayor']=False
    return render(request,"ratios/comparacion-empresas-ratios-promedio.html",{'promedios':promedios,'empresas':empresas,'miempresa':empresa1})

def comparacionRatiosEmpresasValor(request):
    try:
        propietarioemprsa = get_object_or_404(Propietario,user=request.user)

    except:
        print("No hay propietario")

    try:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
        
    except:
        print("No tiene empresa registrada")
    empresas=[]
    ratiosIngresados=[]
    ratiosFinales=[]
    if request.method=="POST":
        razonCirculante=request.POST.get("razonCirculante")
        pruebaAcida=request.POST.get("pruebaAcida")
        razonCapitalTrabajo=request.POST.get("razonCapitalTrabajo")
        razonEfectivo=request.POST.get("razonEfectivo")
        razonRotacionInventario=request.POST.get("razonRotacionInventario")
        razonDiasInventario=request.POST.get("razonDiasInventario")
        razonRotacionCuentasPorCobrar=request.POST.get("razonRotacionCuentasCobrar")
        razonPeriodoMedioCobranza=request.POST.get("razonPeriodoMedioCobranza")
        razonRotacionCuentasPorPagar=request.POST.get("razonRotacionCuentasPagar")
        periodoMedioPago=request.POST.get("periodoMedioPago")
        ratiosIngresados=[
            {"nombre":"Razón circulante","valor":razonCirculante},
            {"nombre":"Prueba ácida","valor":pruebaAcida},
            {"nombre":"Razón de capital de trabajo","valor":razonCapitalTrabajo},
            {"nombre":"Razón de efectivo","valor":razonEfectivo},
            {"nombre":"Razón de rotación de inventario","valor":razonRotacionInventario},
            {"nombre":"Razón de días de inventario","valor":razonDiasInventario},
            {"nombre":"Razón de rotación de cuentas por cobrar","valor":razonRotacionCuentasPorCobrar},
            {"nombre":"Razón de período medio de cobranza","valor":razonPeriodoMedioCobranza},
            {"nombre":"Razón de rotación de cuentas por pagar","valor":razonRotacionCuentasPorPagar},
            {"nombre":"Período medio de pago","valor":periodoMedioPago}
        ]
        anio=2023
        empresa2 = get_object_or_404(Empresa,id=8)
        empresas=[
        {"nombre":emprsa.nombre_empresa},
        {"nombre":empresa2.nombre_empresa}
        ]
        ratios1=funcionRatios(anio,request,None)
        ratios2=funcionRatios(anio,request,empresa2)

        
        for ratioIngresado,ratio1, ratio2 in zip(ratiosIngresados,ratios1, ratios2):
            ratioFinal={}
            if ratioIngresado['valor']:
                ratioFinal['nombre']=ratioIngresado['nombre']
                ratioFinal['ratio1']=ratio1['valor']
                ratioFinal['ratio2']= ratio2['valor']
                ratioFinal['valor']=ratioIngresado['valor']
            
                if ratio1['valor']>=float(ratioIngresado['valor']):
                    ratioFinal['ratio1esMayor']=True
                else:
                    ratioFinal['ratio1esMayor']=False

                if ratio2['valor']>=float(ratioIngresado['valor']):
                    ratioFinal['ratio2esMayor']=True
                else:
                    ratioFinal['ratio2esMayor']=False
                ratiosFinales.append(ratioFinal)
        return render(request,"ratios/comparacionPorValorSalida.html",{"ratios":ratiosFinales,"empresas":empresas,"miempresa":emprsa})
    return render(request,"ratios/comparacionPorValorEntrada.html",{"empresa":emprsa,"ratios":ratiosFinales,"empresas":empresas})

def compararRatiosPorPromedioOvalorIngresa(request):
    pass
