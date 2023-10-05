from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.utils import timezone

import pandas
from django.db.models import Sum
from decimal import Decimal

from .forms import CatalagoForm,EmpresaForm
from .models import Transaccion,Cuenta,Propietario,Empresa


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


def CrearEmpresa(request):

    contexto = {}
    propietario_empresa = request.user.propietario

    if request.method == 'POST':

        form = CatalagoForm(request.POST,
                            request.FILES)
        empresa_form = EmpresaForm(request.POST)
        print(form.errors)
        if form.is_valid() and empresa_form.is_valid():
            #Crear catalogo
            catalago_excel = form.save()
            #get nombre empresa
            nombreempresa = empresa_form.cleaned_data['nombre_empresa']
            #Crear la empresa
            new_empresa = Empresa(nombre_empresa=nombreempresa,
                                  catalogo_empresa=catalago_excel,
                                  propietario=propietario_empresa)
            new_empresa.save()
            #activar la empresa
            p = Propietario.objects.get(user=request.user)
            p.empresactiva = True
            p.save()
            
            #Leer catalogo en excel
            path = f"{settings.MEDIA_ROOT}\{catalago_excel.archivo}"
            data = pandas.read_excel(path,sheet_name="BGN")
            balance = {}
            for index, row in data.iterrows():
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
                    catalago = catalago_excel
                )

                t = Transaccion.objects.create(
                    monto=Decimal(row["valor"]),
                    descripcion="jfksl",
                    slug="kdsa",
                    cuenta=cuenta,
                    fecha_creacion=f"{str(row['anio'])}-10-25 00:00:00",
                    tipo_transaccion="CMP",
                    naturaleza = "DBT"
                )

            contexto["balance"] = "Balance general cargado correctamente"
            return redirect('conta:transaccion-lista')
    else:
        form = CatalagoForm()
        empresa_form = EmpresaForm()
        contexto["form"]=form
        contexto["empresa_form"] = empresa_form 
               
    return render(request,'balances/listar-balance.html',contexto)


def ListarCatalogo(request):
    catalogo = {}
    try:
        catalogo = request.user.propietario.empresa.catalogo_empresa.cuentas.all()
    except:
        print("No hay catalogo")
    return render(request,'catalogo/listar-catalogo.html',{'catalogo':catalogo})
    
