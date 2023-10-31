
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

from .forms import CatalagoForm,EmpresaForm
from .models import Catalogo, Transaccion,Cuenta,Propietario,Empresa
from datetime import date, datetime
import plotly.express as px
import pandas as pd
import base64
import io
from asgiref.sync import sync_to_async
import plotly.graph_objects as go


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
        
    except:
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
        cuentasActivos = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
        print(cuentasActivos)
        for cuenta in cuentasActivos:
            saldoCredito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.CREDITO,
                                                        fecha_creacion__range=(year_1,year_2)
                                                    ).aggregate(total=Sum('monto'))
            saldoDebito = cuenta.transacciones.filter(naturaleza=Transaccion.Naturaleza.DEBITO,
                                                        fecha_creacion__range=(year_1,year_2)
                                                    ).aggregate(total=Sum('monto'))
            if saldoCredito["total"] is None:
                saldoCredito["total"] = Decimal(0.0)
            if saldoDebito["total"] is None:
                saldoDebito["total"] = Decimal(0.0)
            total = saldoDebito["total"] - saldoCredito["total"]
            totalactivos += total 

            diccionario_cuentas[cuenta] = {
            'saldo_credito': saldoCredito["total"],
            'saldo_debito': saldoDebito["total"],
            'total': total
            }

            contexto = {'cuentasActivos': cuentasActivos,
                'totalActivos': total,
                'diccionario_cuentas':diccionario_cuentas,
                'pathbase':settings.BASE_DIR,}
    except:
        print("No tiene empresa registrada aun")

    return render(request,
           'transacciones/lista.html'
           ,contexto)

#HU-002-Registrar empresa con catálogo, BGN Y ERS en formato excel
def CrearEmpresa(request):

    contexto = {}
    
    try:
        propietario_empresa = request.user.propietario
    except:
        print("No tiene Propietario Asignado")
        contexto = {}
        contexto["propietario"] = False
        return render(request,'balances/listar-balance.html',contexto)

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

    return render(request,'balances/listar-balance.html',contexto)

#HU-023-Listar Cuentas del Catalogo
def ListarCatalogo(request):
    catalogo = {}
    try:
        catalogo = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
    except:
        print("No hay catalogo")
    return render(request,'catalogo/listar-catalogo.html',{'catalogo':catalogo})

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
 
    
