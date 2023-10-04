import pandas
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.db.models import Sum
from decimal import Decimal
from .forms import CatalagoForm
from .models import Transaccion,Cuenta
from django.conf import settings
from django.utils import timezone


def lista_transacciones(request):
    totalactivos = 0
    total = 0
    year_1 = ""
    year_2 = ""
    lista_trans = Transaccion.objects.all()
    #Este retorna un query set que debe ser recorrido con un for
    cuentasActivos = Cuenta.cuentas_activos.all()
    diccionario_cuentas = {}
    #Sumar montos #Debo crear un diccionario con la cuenta y monto que tiene
    if request.method == "POST":
        year_1 = request.POST['fechainicio']# retorna como anio-mes-dia
        year_2 = request.POST['fechafinal']# retorna como anio-mes-dia
    else:
        year_1 = timezone.now().strftime('%Y-%m-%d')
        year_2 = timezone.now().strftime('%Y-%m-%d')
        
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
    #revisa si es del lado del debe o del haber para sumar ambos lados y luego restar
    
    contexto = {'cuentasActivos': cuentasActivos,
                'totalActivos': total,
                'diccionario_cuentas':diccionario_cuentas,
                'pathbase':settings.BASE_DIR}

    return render(request,
           'transacciones/lista.html'
           ,contexto)

def CargarBalance(request):

    contexto = {}

    if request.method == 'POST':

        form = CatalagoForm(request.POST,
                            request.FILES)

        if form.is_valid():
            catalago_excel = form.save()
            print()
            #cargar formulario en el cual insertar el nombre del catalogo
            path = f"{settings.MEDIA_ROOT}\{catalago_excel.archivo}"
            data = pandas.read_excel(path,sheet_name="BGN")
            balance = {}
            for index, row in data.iterrows():
                #Extraer primer caracter de la columna codigo
                cod = str(row['codigo'])[0]
                tipo = ''
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
        contexto["form"]=form
               
    return render(request,'balances/listar-balance.html',contexto)


def ListarCatalogo(request):
    catalogo = Cuenta.objects.all()
    return render(request,'catalogo/listar-catalogo.html',{'catalogo':catalogo})
    
