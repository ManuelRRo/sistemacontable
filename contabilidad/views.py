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
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.db.models import Min, Max

#
# Función que puede ser utilizada para identificar al usuario
#
def usuario_identificado(request):
    context = {}
    is_propietario = Propietario.objects.filter(user = request.user).exists()
    if is_propietario:
        propietario = Propietario.objects.filter(user = request.user).first()
        context['propietario'] = propietario
    context['is_propietario'] = is_propietario
    return context


#
# Para mostrar el inicio de la app web
#
@login_required
def home(request):
    context = {}
    propietario = Propietario.objects.filter(user = request.user).first()
    empresa = Empresa.objects.filter(propietario = propietario).first()
    context['propietario'] = propietario
    context['empresa'] = empresa
    return render(request,'home/inicio.html', context)

#
# Para mostrar pantalla de estados financieros
#
@login_required
def estados_financieros(request):
    context = {}
    propietario = Propietario.objects.filter(user = request.user).first()
    empresa = Empresa.objects.filter(propietario = propietario).first()
    context['propietario'] = propietario
    context['empresa'] = empresa
    return render(request,'estados_financieros/home_estados_financieros.html', context)


#HU-19-Grafico de variacion
@sync_to_async
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

#HU-002-Registrar empresa con catálogo, BGN Y ERS en formato excel
def CrearEmpresa(request):

    usuario_identidad = usuario_identificado(request)
    if usuario_identidad['is_propietario']:
        if usuario_identidad['propietario'].empresactiva == 0:
            acceso = 1
        else:
            acceso = 0
    else:
        acceso = 0

    if acceso:
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

                lista_anios = hoja_bgn.columns[3:]
                
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
                        categoria_av = tipo,
                        cuenta_av = row["cuenta_total"],
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
                lista_anios = hoja_ers.columns[3:]

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
                        categoria_av = Cuenta.CategoriaAV.ESTADO_RESULTADOS,
                        cuenta_av = row["cuenta_total"],
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
                return redirect('conta:home')
        else:
            form = CatalagoForm()
            empresa_form = EmpresaForm()
            contexto["form"]=form
            contexto["empresa_form"] = empresa_form 
            contexto["propietario"] = True

        return render(request,'empresa/crear-empresa.html',contexto)
    else:
        messages.error(request, 'Lo sentimos, parece que no tienes acceso')
        return redirect('conta:home')
        
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
# Nueva definir cuentas ratios
#debe ser mismo orden y nombre del urlpatterns definidos en las urls.py

@xframe_options_sameorigin
def updatecuentasRatios(request,id_cuenta_ratio,codigo_ratio):
    context = {}
    cuentas_catalogo = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
    cuenta = None
    if request.method == 'POST':
        print("request.POST",request.POST['cuenta_select'])
        #obtener id del select
        if 'cuenta_select' in request.POST:
            id_nuevo_ratio = request.POST['cuenta_select']
        #obtener objeto cuenta del selesct
        obj = Cuenta.objects.get(pk=id_nuevo_ratio)

        # si no tiene cuenta_ratio asignada
        cuenta_antigua = cuentas_catalogo.filter(cuenta_ratio=codigo_ratio).first()
        print("cuenta antigua",cuenta_antigua)
        if cuenta_antigua == None:
            pass
        else:
            cuenta_antigua.cuenta_ratio = Cuenta.CuentaRatio.NINGUNA
            cuenta_antigua.save()
            
        #asignamos
        obj.cuenta_ratio = codigo_ratio
        #guardar
        obj.save()
        # si tiene cuenta_ratio asignada
        return redirect("conta:crear-cuentas-ratios")

    else:
        if id_cuenta_ratio != 0:
            cuenta = Cuenta.objects.get(pk=id_cuenta_ratio)
        
    context["cuenta_definida"] = cuenta
    context["cuentas_catalogo"] = cuentas_catalogo

    
    print(request)
    return render(request,'ratios/updatecuentaratio.html',context)
        
        
    
#Seleeccionar cuentas ratios
def selectCuentasRatios(request):
    
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
    
    #obtener codigos de ratios menos el NNG
    codigos_ratios = Cuenta.CuentaRatio.values[1:]
    nombres_ratios = Cuenta.CuentaRatio.labels[1:]
    #seleccionar todas las cuentas de ratios
    cuentasCatalogo = usuario.propietario.empresa.catalogo_empresa.cuentas.filter(cuenta_ratio__in=codigos_ratios)
    dict_ratios = {}
    try:
        for nombre,codigo in zip(nombres_ratios,codigos_ratios):
            cuenta_de_ratio = cuentasCatalogo.filter(cuenta_ratio=codigo)
            if len(cuenta_de_ratio) == 0:
                dict_ratios[nombre]={
                "nombre_ratio":nombre,
                "codigo_ratio":codigo,
                "cuenta":cuenta_de_ratio.first(),
                "noasignado":True
                }
            else:
                dict_ratios[nombre]={
                "nombre_ratio":nombre,
                "codigo_ratio":codigo,
                "cuenta":cuenta_de_ratio.first(),
                "noasignado":False
                }
    except Exception as e:
        pass
    print(cuentasCatalogo)
    context = {
        "dict_ratios":dict_ratios,
    }

    return render(request,'ratios/select-ratios.html',context)

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
                print("valor request al select 1",request.POST)
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
    usuario_identidad = usuario_identificado(request)
    if usuario_identidad['is_propietario']:
        if usuario_identidad['propietario'].empresactiva == 1:
            acceso = 1
        else:
            acceso = 0
    else:
        acceso = 0
    
    if acceso:
        catalogo = {}
        try:
            catalogo = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
        except:
            print("No hay catalogo")
        return render(request,'catalogo/listar-catalogo.html',{'catalogo':catalogo})
    else:
        messages.error(request, 'Lo sentimos, parece que no tienes acceso')
        return redirect('conta:home')

    

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
    year_1 = ""
    year_2 = ""
    
    #Sumar montos #Debo crear un diccionario con la cuenta y monto que tiene
    if request.method == "POST":
        try:
            #la fecha debe ser de tipo datetime.date(anio,mes,dia)
            year_1 = datetime.strptime(request.POST['fechainicio'], "%Y-%m-%d")# retorna como anio-mes-dia
            year_2 = datetime.strptime(request.POST['fechafinal'], "%Y-%m-%d")# retorna como anio-mes-dia
            rango_de_anios = [str(anio) for anio in range(year_1.year, year_2.year + 1)]

            contexto = sumarTransacciones(request,rango_de_anios,year_1,year_2)

            print("contexto_)sumas",contexto)
        except Exception as e:
            error_message = f"Se produjo una excepción: {str(e)}"
            print(error_message)
            print("Problema en sumar Trasnsacciones")
        return render(request,'balance/listar-balance.html',contexto)
    else:
        try:
            year_1 = timezone.now().strftime('%Y-%m-%d')
            year_2 = timezone.now().strftime('%Y-%m-%d')

        
            contexto = sumarTransacciones(request,rango_de_anios,op=0)
        except Exception as e:
            error_message = f"Se produjo una excepción: {str(e)}"
            print(error_message)

        return render(request,'balance/listar-balance.html',contexto)
    
#Funcion que no se usa
# def seleccionar_trans_cate(categoria, anio,request_,total_cuenta):
#         lista = []
#         cuentas = request_.user.propietario.empresa.catalogo_empresa.cuentas.all()
#         for cuenta in cuentas.filter(categoria=Cuenta.Categoria.ACTIVO):
#             #print("cuenta: ", (cuenta.transacciones.all().filter(fecha_creacion__year=2022).first().monto/total_cuenta)*100)     
#             lista.append((cuenta.transacciones.all().filter(fecha_creacion__year=2022).first().monto/total_cuenta)*100)   
#         return lista

def sumarTransacciones(request,rango_anios,year_1=None,year_2=None,year_3=None,op=1):
    cuentasActivos = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
    diccionario_cuentas = {}
    contexto = {}
    totalactivos = 0
    total_activos = 0
    total_pasivos = 0
    total_capital = 0
    total_ventas = 0
    total = 0
    anio_1 = ""
    anio_2 = ""
    anio_3 = ""
    id_transaccion = 0
    a = 0
    
    if op == 1:
        anio_1 = year_1.date()
        anio_2 = year_2.date()
        anio_3 = year_3
    else:
        #date(anio,mes,dia)
        anio_1 = date(timezone.now().year,1,1)
        anio_2 = date(timezone.now().year,12,31)
        anio_3 = timezone.now().year
        #print("tip y valor",type(anio_1),anio_1)
        
    for cuenta in cuentasActivos:

        saldoCredito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.CREDITO,
                                                    fecha_creacion__range=(anio_1,anio_2)
                                                ).aggregate(total=Sum('monto'))



        saldoDebito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.DEBITO,
                                                    fecha_creacion__range=(anio_1,anio_2)
                                                ).aggregate(total=Sum('monto'))
        
        if saldoCredito["total"] is None:
            saldoCredito["total"] = Decimal(0.0)
        if saldoDebito["total"] is None:
            saldoDebito["total"] = Decimal(0.0)
        total = saldoDebito["total"] - saldoCredito["total"]
        totalactivos += total

        cnt = cuenta.transacciones.filter(Q(naturaleza=Transaccion.Naturaleza.DEBITO) | Q(naturaleza=Transaccion.Naturaleza.CREDITO),fecha_creacion__range=(anio_1,anio_2))
        # try:
        #     id_trans = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.DEBITO,
        #                                            fecha_creacion__range=(anio_1,anio_2))
        #     if len(id_trans) != 0:
        #         id_transaccion = id_trans[0]
        #         print("Valor id trans",id_transaccion.)
        # except Exception as e:
        #     error_message = f"Se produjo una excepción: {str(e)}"
        #     print("saldo debito pk",type(id_trans))
        #     print(error_message)

        diccionario_cuentas[cuenta] = {
        'saldo_credito': saldoCredito["total"],
        'saldo_debito': saldoDebito["total"],
        'total': total,
        'num_cuenta': cnt.first().pk,
        }
         
    contexto = {'cuentasActivos': cuentasActivos,
        'totalActivos': total,
        'diccionario_cuentas':diccionario_cuentas,
        'pathbase':settings.BASE_DIR,
        'anio' : anio_3,
        'rango_anios': rango_anios
        }
        
    return contexto

def calculoAVertical(request,year_1=None,year_2=None,year_3=None,op=1):
    cuentasActivos = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
    diccionario_cuentas = {}
    contexto = {}
    totalactivos = 0
    anio_1 = ""
    anio_2 = ""
    anio_3 = ""
    id_transaccion = 0
    b = 0
    c = 0
    
    if op == 1:
        anio_1 = year_1
        anio_2 = year_2
        anio_3 = year_3
    else:
        #date(anio,mes,dia)
        anio_1 = date(timezone.now().year,1,1)
        anio_2 = date(timezone.now().year,12,31)
        anio_3 = timezone.now().year
        #print("tip y valor",type(anio_1),anio_1)
        
    for cuenta in cuentasActivos:

        #HU-06 Analisis Vertical
        try:
            total_activos = cuentasActivos.filter(cuenta_av=Cuenta.CuentaAV.TOTAL_ACTIVOS).first().transacciones.filter(fecha_creacion__range=(anio_1,anio_2)).first().monto
            total_pasivos = cuentasActivos.filter(cuenta_av=Cuenta.CuentaAV.TOTAL_PASIVOS).first().transacciones.filter(fecha_creacion__range=(anio_1,anio_2)).first().monto
            total_capital = cuentasActivos.filter(cuenta_av=Cuenta.CuentaAV.TOTAL_CAPITAL).first().transacciones.filter(fecha_creacion__range=(anio_1,anio_2)).first().monto
            total_ventas = cuentasActivos.filter(cuenta_av=Cuenta.CuentaAV.VENTAS_TOTALES).first().transacciones.filter(fecha_creacion__range=(anio_1,anio_2)).first().monto
        except Exception as e:
            error_message = f"Se produjo una excepción: {str(e)}"
            print(error_message)

        saldoCredito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.CREDITO,
                                                    fecha_creacion__range=(anio_1,anio_2)
                                                ).aggregate(total=Sum('monto'))


        saldoDebito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.DEBITO,
                                                    fecha_creacion__range=(anio_1,anio_2)
                                                ).aggregate(total=Sum('monto'))
        
        if saldoCredito["total"] is None:
            saldoCredito["total"] = Decimal(0.0)
        if saldoDebito["total"] is None:
            saldoDebito["total"] = Decimal(0.0)
        total = saldoDebito["total"] - saldoCredito["total"]
        totalactivos += total

        #HU-06 Analisis Vertical
        cnt = cuenta.transacciones.filter(Q(naturaleza=Transaccion.Naturaleza.DEBITO) | Q(naturaleza=Transaccion.Naturaleza.CREDITO),fecha_creacion__range=(anio_1,anio_2))
        # print("Cuenta: ",cuenta, "Monto: ", saldoDebito/)
        if cuenta.categoria_av == Cuenta.CategoriaAV.ACTIVO:
            #print("Cuenta: ",cuenta.nombre,cnt.first().monto,"Vertical",(cnt.first().monto/total_activos)*100)
            a = (cnt.first().monto/total_activos)*100
        if cuenta.categoria_av == Cuenta.CategoriaAV.PASIVO:
            #print("Cuenta: ",cuenta.nombre,cnt.first().monto,"Vertical",(cnt.first().monto/total_pasivos)*100)
            a = (cnt.first().monto/total_pasivos)*100
        if cuenta.categoria_av == Cuenta.CategoriaAV.PATRIMONIO:
            #print("Cuenta: ",cuenta.nombre,cnt.first().monto,"Vertical",(cnt.first().monto/total_capital)*100)
            a = (cnt.first().monto/total_capital)*100
        if cuenta.categoria_av == Cuenta.CategoriaAV.ESTADO_RESULTADOS:
            #print("Cuenta: ",cuenta.nombre,cnt.first().monto,"Vertical",(cnt.first().monto/total_capital)*100)
            a = (cnt.first().monto/total_ventas)*100


        #print("Nombre cuenta:", cuenta.nombre)
        #print("Saldo 2023:", saldo_aniomayor)
        #print("Saldo 2022:", saldo_aniomenor)
        #print("Análisis Horizontal:", b)

        diccionario_cuentas[cuenta] = {
        'saldo_credito': saldoCredito["total"],
        'saldo_debito': saldoDebito["total"],
        'total': total,
        'num_cuenta': cnt.first().pk,
        'av': round(a,2),
        }
         
    contexto = {'cuentasActivos': cuentasActivos,
        'totalActivos': total,
        'diccionario_cuentas':diccionario_cuentas,
        'pathbase':settings.BASE_DIR,
        }
        
    return contexto

#HU-06 Analisis Vertical
@login_required
def analisisVertical(request):
    context={}
    try:
        year_1 = datetime.strptime(request.POST['fechainicio'], "%Y-%m-%d").date()# retorna como anio-mes-dia
        year_2 = datetime.strptime(request.POST['fechafinal'], "%Y-%m-%d").date()# retorna como anio-mes-dia
        year_3 = datetime.strptime(request.POST['fechainicio'], "%Y-%m-%d").year

        context = calculoAVertical(request,year_1,year_2,year_3,op=1)
    except Exception as e:
        error_message = f"Se produjo una excepción: {str(e)}"
        #print(error_message)
        messages.error(request, f'Seleccione una fecha')
    return render(request,'analisis_vertical/analisis_vertical.html',context)


#HU-07 Analisis Horizontal
def calculoAHorizontal(request,year_1=None,year_2=None,year_3=None,op=1):
    cuentasActivos = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
    diccionario_cuentas = {}
    contexto = {}
    totalactivos = 0
    anio_1 = ""
    anio_2 = ""
    anio_3 = ""
    id_transaccion = 0
    b = 0
    c = 0
    
    if op == 1:
        anio_1 = year_1
        anio_2 = year_2
        anio_3 = year_3
    else:
        #date(anio,mes,dia)
        anio_1 = date(timezone.now().year,1,1)
        anio_2 = date(timezone.now().year,12,31)
        anio_3 = timezone.now().year
        #print("tip y valor",type(anio_1),anio_1)
        
    for cuenta in cuentasActivos:

        saldoCredito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.CREDITO,
                                                    fecha_creacion__range=(anio_1,anio_2)
                                                ).aggregate(total=Sum('monto'))


        saldoDebito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.DEBITO,
                                                    fecha_creacion__range=(anio_1,anio_2)
                                                ).aggregate(total=Sum('monto'))
        
        if saldoCredito["total"] is None:
            saldoCredito["total"] = Decimal(0.0)
        if saldoDebito["total"] is None:
            saldoDebito["total"] = Decimal(0.0)
        total = saldoDebito["total"] - saldoCredito["total"]
        totalactivos += total

        # Obtén el saldo de la cuenta en el anio menor
        saldo_aniomenor = Transaccion.objects.filter(cuenta=cuenta, fecha_creacion__year=year_1.year).first().monto
        # Obtén el saldo de la cuenta en el anio mayor
        saldo_aniomayor = Transaccion.objects.filter(cuenta=cuenta, fecha_creacion__year=year_2.year).first().monto

        # Calcula el análisis horizontal variacion absoluta
        b = saldo_aniomayor - saldo_aniomenor
        #Calcular el análisis horizontal variacion relativa
        if saldo_aniomenor != 0:
            c = ((saldo_aniomayor / saldo_aniomenor) - 1) * 100
        else:
            c = 0

        #print("Nombre cuenta:", cuenta.nombre)
        #print("Saldo 2023:", saldo_aniomayor)
        #print("Saldo 2022:", saldo_aniomenor)
        #print("Análisis Horizontal:", b)

        diccionario_cuentas[cuenta] = {
        'saldo_credito': saldoCredito["total"],
        'saldo_debito': saldoDebito["total"],
        'total': total,
        'num_cuenta': 0,#id_transaccion.pk,
        'ahVA': round(b,2),
        'ahVR': round(c,2),
        }
         
    contexto = {'cuentasActivos': cuentasActivos,
        'totalActivos': total,
        'diccionario_cuentas':diccionario_cuentas,
        'pathbase':settings.BASE_DIR,
        }
        
    return contexto


#HU-07 Analisis Horizontal
@login_required
def analisisHorizontal(request):
    context={}
    try:
        year_1 = datetime.strptime(request.POST['fechainicio'], "%Y-%m-%d").date()# retorna como anio-mes-dia
        year_2 = datetime.strptime(request.POST['fechafinal'], "%Y-%m-%d").date()# retorna como anio-mes-dia
        context = calculoAHorizontal(request,year_1,year_2,op=1)
    except Exception as e:
        error_message = f"Se produjo una excepción: {str(e)}"
        print(error_message)
        messages.error(request, f'Seleccione una fecha')
    return render(request,'analisis_horizontal/analisis_horizontal.html',context)

class TransaccionUpdateView(UpdateView):
    model = Transaccion
    form_class = UpdateTransaccionForm
    template_name = 'balance/transaccion_update.html'
    success_url = reverse_lazy('conta:ver_balance_general')

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
        print("transaccion cuenta",transaccion_cuenta)
       # Crear un diccionario para almacenar transacciones por año
        transacciones_por_anio = {}

        for anio in rango_de_anios:
            transacciones_por_anio[anio] = []
        print("transaccion_por_anio",transacciones_por_anio)

        for transaccion in transaccion_cuenta:
            anio_transaccion = str(transaccion.fecha_creacion.year)
            if anio_transaccion in transacciones_por_anio:
                transacciones_por_anio[anio_transaccion].append(transaccion)
        print("transaccion_por_anio 2",transacciones_por_anio)
        context["transacciones_por_anio"] = transacciones_por_anio
        context["empresa"] = self.get_context_data()["empresa"]
        context["fecha_inicio"] = fecha_inicio
        context["fecha_final"] = fecha_final
        context["rango_de_anios"] = rango_de_anios
        context["cuentas"] = transacciones_por_anio[rango_de_anios[0]]
        

        return render(request, self.template_name, context) 
    
class VerBalanceGeneral(View):
    model_transaccion = Transaccion
    model_empresa = Empresa
    template_name = 'balance/listar-balance2.html'

    def get_queryset(self):
        context = {}
        empresa = self.model_empresa.objects.get(propietario__user=self.request.user)
        # Crear tres objetos Q, uno para cada categoría
        q1 = Q(cuenta__categoria=Cuenta.Categoria.ACTIVO)
        q2 = Q(cuenta__categoria=Cuenta.Categoria.PASIVO)
        q3 = Q(cuenta__categoria=Cuenta.Categoria.PATRIMONIO)
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
        print("transaccion cuenta",transaccion_cuenta)
       # Crear un diccionario para almacenar transacciones por año
        transacciones_por_anio = {}

        for anio in rango_de_anios:
            transacciones_por_anio[anio] = []
        print("transaccion_por_anio",transacciones_por_anio)

        for transaccion in transaccion_cuenta:
            anio_transaccion = str(transaccion.fecha_creacion.year)
            if anio_transaccion in transacciones_por_anio:
                transacciones_por_anio[anio_transaccion].append(transaccion)
        print("transaccion_por_anio 2",transacciones_por_anio)
        context["transacciones_por_anio"] = transacciones_por_anio
        context["empresa"] = self.get_context_data()["empresa"]
        context["fecha_inicio"] = fecha_inicio
        context["fecha_final"] = fecha_final
        context["rango_de_anios"] = rango_de_anios
        context["cuentas"] = transacciones_por_anio[rango_de_anios[0]]
        

        return render(request, self.template_name, context)

def funcionRatios(anio,request,emprsa):
    # Obtener el propietario de la empresa
    propietarioemprsa = get_object_or_404(Propietario,user=request.user)
    if emprsa is None:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
    
    # Cuentas necesarias para calcular ratios financieros
    activoCorriente = Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    pasivoCorriente = Transaccion.objects.filter(cuenta__cuenta_ratio="PSVC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    inventario = Transaccion.objects.filter(cuenta__cuenta_ratio="INVT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    activosTotales = Transaccion.objects.filter(cuenta__cuenta_ratio="ACTV", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    efectivo = Transaccion.objects.filter(cuenta__cuenta_ratio="EFCT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    valoresCortoPlazo = Transaccion.objects.filter(cuenta__cuenta_ratio="VLRS", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    costoDeVenta = Transaccion.objects.filter(cuenta__cuenta_ratio="CSTDV", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    ventasNetas = Transaccion.objects.filter(cuenta__cuenta_ratio="VNTSN", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    cuentasPorPagarComerciales = Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPP", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    cuentasPorCobrarComerciales = Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto    
    cuentasPorCobrarComercialesAnterior = Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio-1).first()  
    cuentasPorPagarComercialesAnterior = Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPP", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio-1).first()   
    inventarioAnterior = Transaccion.objects.filter(cuenta__cuenta_ratio="INVT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio-1).first()
    compras = Transaccion.objects.filter(cuenta__cuenta_ratio="CSTDV", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    
    # Razon Circulante
    razonCirculante = activoCorriente/pasivoCorriente
    # Prueba Acida
    pruebaAcida=(activoCorriente-inventario)/pasivoCorriente
    # Razon de Capital de Trabajo
    razonCapitalTrabajo=(activoCorriente-pasivoCorriente)/activosTotales
    # Razon de Efectivo
    razonEfectivo=(efectivo+valoresCortoPlazo)/pasivoCorriente
    # Razon de Rotacion de Inventario y Dias de Inventario
    if inventarioAnterior:
        razonRotacionInventario = costoDeVenta /((inventario+inventarioAnterior.monto)/2)
        razonDiasInventario = ((inventario+inventarioAnterior.monto)/2)/(costoDeVenta/365)
    else:
        razonRotacionInventario = costoDeVenta/inventario
        razonDiasInventario = inventario/(costoDeVenta/365)
    # Razon de Rotacion de Cuentas por Cobrar y Periodo Medio de Cobranza
    if cuentasPorCobrarComercialesAnterior:
        razonRotacionCuentasPorCobrar=ventasNetas/((cuentasPorCobrarComerciales+cuentasPorCobrarComercialesAnterior.monto)/2)
        razonPeriodoMedioCobranza=(((cuentasPorCobrarComerciales+cuentasPorCobrarComercialesAnterior.monto)/2)*365)/ventasNetas
    else:
        razonRotacionCuentasPorCobrar=ventasNetas/cuentasPorCobrarComerciales
        razonPeriodoMedioCobranza=(cuentasPorCobrarComerciales*365)/ventasNetas
    # Razon de Rotacion de Cuentas por Pagar y Periodo Medio de Pago
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

@login_required
def calcular_ratios(request):
    try:
        propietarioemprsa = get_object_or_404(Propietario,user=request.user)

    except:
        print("No hay propietario")

    try:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
        
    except:
        print("No tiene empresa registrada")
    anios=[]
    ratios=[]
    anio=None
    activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=emprsa.catalogo_empresa).order_by("fecha_creacion")
    if activoCorriente:
        for activo in activoCorriente:
            anioNuevo={"anio":activo.fecha_creacion.year} 
            anios.append(anioNuevo)
    if request.method=="POST":
        anio=int(request.POST.get("selectAño"))
        ratios=funcionRatios(anio,request,None)    
        #Sumar montos #Debo crear un diccionario con la cuenta y monto que tiene
        """
        if request.method == "POST":
            year_1 = request.POST['fechainicio']# retorna como anio-mes-dia
            year_2 = request.POST['fechafinal']# retorna como anio-mes-dia
        else:
            year_1 = timezone.now().strftime('%Y-%m-%d')
            year_2 = timezone.now().strftime('%Y-%m-%d')  
        """
    return render(request,"ratios/calcular-ratios.html",{'ratios':ratios,'empresa':emprsa,"listaAños":anios,"anio":anio})

@login_required
def comparacionRatiosEmpresasPromedio(request):
    try:
        propietarioemprsa = get_object_or_404(Propietario,user=request.user)

    except:
        print("No hay propietario")

    try:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
            
    except:
        print("No tiene empresa registrada")
    empresa2=None
    anio=None
    error=None
    anios=[]
    listaAimprimir=[]
    empresasSector=[]
    empresaSeleccionada=None
    #ratiosEmpresas=[]
    empresasSector=Empresa.objects.filter(sector=emprsa.sector)
    activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=emprsa.catalogo_empresa).order_by("fecha_creacion")
    if activoCorriente:
        for activo in activoCorriente:
            anioNuevo={"anio":activo.fecha_creacion.year} 
            anios.append(anioNuevo)
    else:
        error="Error, la empresa "+str(emprsa)+" no tiene asignadas cuentas para el cálculo de ratios"
    if request.method=="POST":
        empresaSeleccionada=request.POST.get('selectEmpresa')
        anio=int(request.POST.get("selectAño"))
        empresa2 = get_object_or_404(Empresa,id=empresaSeleccionada)
        activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=emprsa.catalogo_empresa).first()
        activoCorriente2=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=empresa2.catalogo_empresa).first()
        activoCorriente2Fecha=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=empresa2.catalogo_empresa,fecha_creacion__year=anio).first()
        if activoCorriente2 and activoCorriente2Fecha:
            """""
            empresaSeleccionada=request.POST.getlist('empresasSeleccionadas')
            for empresaId in empresaSeleccionada:
                empresa = get_object_or_404(Empresa,id=empresaId)
                ratios=funcionRatios(anio,request,empresa)
                elemento={"empresa.id":empresa.id,"ratios":ratios}
                ratiosEmpresas.append(ratios)
            """
            try:   
                ratios1=funcionRatios(anio,request,emprsa)
                ratios2=funcionRatios(anio,request,empresa2)
            except:
                error="Error, asegurese de que todas las cuentas tengan montos en los años requeridos. Mientras tanto, elija otro año u otra empresa"
                contexto={'listaAimprimir':listaAimprimir,'miempresa':emprsa,"empresa2":empresa2,"listaAños":anios,"anio":anio,"empresasSector":empresasSector,"error":error}
                return render(request,"ratios/comparacion-empresas-ratios-promedio.html",contexto)
                    
            listaAimprimir=[
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
            for elemento,ratio1, ratio2 in zip(listaAimprimir,ratios1, ratios2):
                valorDeComparacion=(ratio1['valor'] + ratio2['valor']) / 2

                elemento['ratio1']=ratio1['valor']
                elemento['ratio2']= ratio2['valor']
                elemento['valorDeComparacion']=valorDeComparacion
                    
                if ratio1['valor']>=valorDeComparacion:
                    elemento['ratio1esMayor']=True
                else:
                    elemento['ratio1esMayor']=False

                if ratio2['valor']>=valorDeComparacion:
                        elemento['ratio2esMayor']=True
                else:
                    elemento['ratio2esMayor']=False
        else:
            if activoCorriente2Fecha is None:
                error="Error, la empresa "+str(empresa2) +" no tiene transacciones en el año seleccionado"
            if activoCorriente2 is None:
                error="Error, la empresa "+str(empresa2) +" no tiene asignadas cuentas para el cálculo de ratios"
    contexto={'listaAimprimir':listaAimprimir,'miempresa':emprsa,"empresa2":empresa2,"listaAños":anios,"anio":anio,"empresasSector":empresasSector,"error":error}
    return render(request,"ratios/comparacion-empresas-ratios-promedio.html",contexto)

@login_required
def comparacionRatiosEmpresasValor(request):
    try:
        propietarioemprsa = get_object_or_404(Propietario,user=request.user)

    except:
        print("No hay propietario")

    try:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
            
    except:
        print("No tiene empresa registrada")
    empresa2=None
    anio=None
    error=None
    anios=[]
    listaAimprimir=[]
    empresasSector=[]
    ratiosIngresados=[]
    empresaSeleccionada=None
    #ratiosEmpresas=[]
    empresasSector=Empresa.objects.filter(sector=emprsa.sector)
    activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=emprsa.catalogo_empresa).order_by("fecha_creacion")
    if activoCorriente:
        for activo in activoCorriente:
            anioNuevo={"anio":activo.fecha_creacion.year} 
            anios.append(anioNuevo)
    else:
        error="Error, la empresa "+str(emprsa)+" no tiene asignadas cuentas para el cálculo de ratios"
    if request.method=="POST":
        empresaSeleccionada=request.POST.get('selectEmpresa')
        anio=int(request.POST.get("selectAño"))
        empresa2 = get_object_or_404(Empresa,id=empresaSeleccionada)
        activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=emprsa.catalogo_empresa).first()
        activoCorriente2=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=empresa2.catalogo_empresa).first()
        activoCorriente2Fecha=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=empresa2.catalogo_empresa,fecha_creacion__year=anio).first()
        if activoCorriente2 and activoCorriente2Fecha:
            """""
            empresaSeleccionada=request.POST.getlist('empresasSeleccionadas')
            for empresaId in empresaSeleccionada:
                empresa = get_object_or_404(Empresa,id=empresaId)
                ratios=funcionRatios(anio,request,empresa)
                elemento={"empresa.id":empresa.id,"ratios":ratios}
                ratiosEmpresas.append(ratios)
            """
            try:   
                ratios1=funcionRatios(anio,request,emprsa)
                ratios2=funcionRatios(anio,request,empresa2)
            except:
                error="Error, asegurese de que todas las cuentas tengan montos en los años requeridos. Mientras tanto, elija otro año u otra empresa"
                contexto={'listaAimprimir':listaAimprimir,'miempresa':emprsa,"empresa2":empresa2,"listaAños":anios,"anio":anio,"empresasSector":empresasSector,"error":error}
                return render(request,"ratios/comparacionPorValorSalida.html",contexto)
                    
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
            
            for ratioIngresado,ratio1, ratio2 in zip(ratiosIngresados,ratios1, ratios2):
                ratioFinal={}
                if ratioIngresado['valor']:
                    ratioFinal['nombre']=ratioIngresado['nombre']
                    ratioFinal['ratio1']=ratio1['valor']
                    ratioFinal['ratio2']= ratio2['valor']
                    ratioFinal['valorDeComparacion']=ratioIngresado['valor']
                
                    if ratio1['valor']>=float(ratioIngresado['valor']):
                        ratioFinal['ratio1esMayor']=True
                    else:
                        ratioFinal['ratio1esMayor']=False

                    if ratio2['valor']>=float(ratioIngresado['valor']):
                        ratioFinal['ratio2esMayor']=True
                    else:
                        ratioFinal['ratio2esMayor']=False
                    listaAimprimir.append(ratioFinal)
        else:
            if activoCorriente2Fecha is None:
                error="Error, la empresa "+str(empresa2) +" no tiene transacciones en el año seleccionado"
            if activoCorriente2 is None:
                error="Error, la empresa "+str(empresa2) +" no tiene asignadas cuentas para el cálculo de ratios"
        contexto={'listaAimprimir':listaAimprimir,'miempresa':emprsa,"empresa2":empresa2,"listaAños":anios,"anio":anio,"empresasSector":empresasSector,"error":error}
        return render(request,"ratios/comparacionPorValorSalida.html",contexto)
    contexto={"empresasSector":empresasSector,"miempresa":emprsa, "listaAños":anios,"error":error,"ratiosIngresados":ratiosIngresados}
    return render(request,"ratios/comparacionPorValorEntrada.html",contexto)

#
# HU-11: Comparación de Empresas VS Ratio Financiero/Promedio
#
class Benchmark(View):

    template_name = 'ratios/benchmark.html'

    def get_queryset(self):
        context = {}
        context['sectores'] = Empresa.Sector.choices
        return context
    
    def get_context_data(self, **kwargs):
        context = {}
        context.update(self.get_queryset()) 
        return context

    def get(self, request, *args, **kwargs):
        context = {}
        context.update(self.get_context_data())
        return render(request, self.template_name,context)
    
    def post(self, request, *args, **kwargs):
        context = {}
        context.update(self.get_context_data())
        # Obteniendo datos del formulario
        nombre_Ratio = str(request.POST.get('select_Ratio', None))
        codigo_Sector = request.POST.get('select_Sector', None)
        anio_benchmark = int (request.POST.get('anio_benchmark', None))

        # Empresas que pertenecen al sector
        empresas = Empresa.objects.filter(sector = codigo_Sector)

        # Para calcular el promedio del ratio financiero
        promedio_ratio = 0
        try:
            if empresas.first():
                empresa_ratio = []
                for empresa in empresas:
                    recibe_ratios = calcula_ratiosFin(anio_benchmark, empresa)
                    for ratio in recibe_ratios:
                        if ratio['nombre'] == nombre_Ratio:
                            ratio_calculado = round(ratio['valor'], 2)
                            promedio_ratio += ratio_calculado
                    empresa_ratio.append({'empresa':empresa, 'valor': ratio_calculado})

            # Calculando el promedio del ratio financiero
            promedio_ratio = promedio_ratio/len(empresas)

            # Diccionario destinado para template
            context['empresas'] = empresa_ratio
            context['promedio_ratio'] = round(promedio_ratio,2)
            context['nombre_ratio'] = nombre_Ratio.upper()
            context['nombre_sector'] = empresas.first().sector
            context['anio_benchmark'] = anio_benchmark
            return render(request, self.template_name, context)
        except:
            messages.error(request, 'Lo sentimos, no fue posible ejecutar la instrucción')
            return redirect('conta:ver_benchmark')

#
# Calcula los ratios como la función anterior, con la única
# diferencia que en parametros tiene una variación
#
def calcula_ratiosFin(anio, empresa):
    emprsa = Empresa.objects.get(id = empresa.id)
    
    # Cuentas necesarias para calcular ratios financieros
    activoCorriente = Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    pasivoCorriente = Transaccion.objects.filter(cuenta__cuenta_ratio="PSVC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    inventario = Transaccion.objects.filter(cuenta__cuenta_ratio="INVT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    activosTotales = Transaccion.objects.filter(cuenta__cuenta_ratio="ACTV", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    efectivo = Transaccion.objects.filter(cuenta__cuenta_ratio="EFCT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    valoresCortoPlazo = Transaccion.objects.filter(cuenta__cuenta_ratio="VLRS", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    costoDeVenta = Transaccion.objects.filter(cuenta__cuenta_ratio="CSTDV", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    ventasNetas = Transaccion.objects.filter(cuenta__cuenta_ratio="VNTSN", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio).first().monto
    cuentasPorPagarComerciales = Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPP", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    cuentasPorCobrarComerciales = Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto    
    cuentasPorCobrarComercialesAnterior = Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPC", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio-1).first()  
    cuentasPorPagarComercialesAnterior = Transaccion.objects.filter(cuenta__cuenta_ratio="CNTAPP", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio-1).first()   
    inventarioAnterior = Transaccion.objects.filter(cuenta__cuenta_ratio="INVT", cuenta__catalogo=emprsa.catalogo_empresa, fecha_creacion__year=anio-1).first()
    compras = Transaccion.objects.filter(cuenta__cuenta_ratio="CSTDV", cuenta__catalogo=emprsa.catalogo_empresa,fecha_creacion__year=anio).first().monto
    
    # Razon Circulante
    razonCirculante = activoCorriente/pasivoCorriente
    # Prueba Acida
    pruebaAcida=(activoCorriente-inventario)/pasivoCorriente
    # Razon de Capital de Trabajo
    razonCapitalTrabajo=(activoCorriente-pasivoCorriente)/activosTotales
    # Razon de Efectivo
    razonEfectivo=(efectivo+valoresCortoPlazo)/pasivoCorriente
    # Razon de Rotacion de Inventario y Dias de Inventario
    if inventarioAnterior:
        razonRotacionInventario = costoDeVenta /((inventario+inventarioAnterior.monto)/2)
        razonDiasInventario = ((inventario+inventarioAnterior.monto)/2)/(costoDeVenta/365)
    else:
        razonRotacionInventario = costoDeVenta/inventario
        razonDiasInventario = inventario/(costoDeVenta/365)
    # Razon de Rotacion de Cuentas por Cobrar y Periodo Medio de Cobranza
    if cuentasPorCobrarComercialesAnterior:
        razonRotacionCuentasPorCobrar=ventasNetas/((cuentasPorCobrarComerciales+cuentasPorCobrarComercialesAnterior.monto)/2)
        razonPeriodoMedioCobranza=(((cuentasPorCobrarComerciales+cuentasPorCobrarComercialesAnterior.monto)/2)*365)/ventasNetas
    else:
        razonRotacionCuentasPorCobrar=ventasNetas/cuentasPorCobrarComerciales
        razonPeriodoMedioCobranza=(cuentasPorCobrarComerciales*365)/ventasNetas
    # Razon de Rotacion de Cuentas por Pagar y Periodo Medio de Pago
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

def calcular_ratios2(request):
    try:
        propietarioemprsa = get_object_or_404(Propietario,user=request.user)

    except:
        print("No hay propietario")

    try:
        emprsa = get_object_or_404(Empresa,propietario=propietarioemprsa)
        
    except:
        print("No tiene empresa registrada")
    anios=[]
    anio1=None
    anio2=None
    error=None
    listaAimprimir=[]
    activoCorriente=Transaccion.objects.filter(cuenta__cuenta_ratio="ACTC",cuenta__catalogo=emprsa.catalogo_empresa).order_by("fecha_creacion")
    if activoCorriente:
        for activo in activoCorriente:
            anioNuevo={"anio":activo.fecha_creacion.year} 
            anios.append(anioNuevo)
    else:
        error="Error, la empresa "+str(emprsa)+" no tiene asignadas cuentas para el cálculo de ratios"
    if request.method=="POST":
        anio2=int(request.POST.get("selectAño1"))
        anio1=anio2-1
        listaAimprimir=[
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
        try:
            ratios1=funcionRatios(anio1,request,None)
            ratios2=funcionRatios(anio2,request,None)
        except:
            error="Error, asegurese de que todas las cuentas tengan montos en los años requeridos. Mientras tanto, elija otro año u otra empresa"
            contexto={'empresa':emprsa,"listaAños":anios,"anio1":anio1,"anio2":anio2,"listaAimprimir":listaAimprimir,"error":error}
            return render(request,"ratios/calcular-ratios copy.html",contexto)
        for elemento,ratio1, ratio2 in zip(listaAimprimir,ratios1, ratios2):
                elemento['ratio1']=ratio1['valor']
                elemento['ratio2']= ratio2['valor']
                if ratio1['valor']>=ratio2['valor']:
                    elemento['ratio1esMayor']=True
                else:
                    elemento['ratio1esMayor']=False
    contexto={'empresa':emprsa,"listaAños":anios,"anio1":anio1,"anio2":anio2,"listaAimprimir":listaAimprimir,"error":error}
    return render(request,"ratios/calcular-ratios copy.html",contexto)
