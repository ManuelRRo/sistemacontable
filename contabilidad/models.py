from django.db import models
from django.utils import timezone
from django.conf import settings

# Managers

class CuentasDebeManager(models.Manager):
     def get_queryset(self):
         return super().get_queryset()\
         .filter(categoria=Cuenta.Categoria.ACTIVO)

class CuentasHaberManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
        .filter(categoria=Cuenta.Categoria.PASIVO)



#HU-02 Modulo de registros de empresa
class Propietario(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    empresactiva = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user.username}'

class Catalogo(models.Model):
    nombre_catalogo = models.CharField(max_length=255,blank=True, default="catalogo")
    archivo = models.FileField(upload_to='archivos_excel/',blank=False)
    
    def __str__(self):
        return self.nombre_catalogo

class Empresa(models.Model):

    class Sector(models.TextChoices):
        MINERA = 'MNR','Minería'
        TURISMO = 'TRM','Turismo'

    nombre_empresa = models.CharField(max_length=255,blank=False)
    sector = models.CharField(max_length=5,choices=Sector.choices,default=Sector.MINERA)
    catalogo_empresa = models.OneToOneField(Catalogo,
                                   on_delete=models.CASCADE,
                                   )
    propietario = models.OneToOneField(Propietario,
                                       on_delete=models.CASCADE,
                                       )
    
    
    
    def __str__(self):
        return self.nombre_empresa


#HU-01 Modulo de Cuentas
class Cuenta(models.Model):

    class Categoria(models.TextChoices):
        BALANCE_GENERAL = 'BAG','Balance General'
        ACTIVO='ASV','Activo'
        PASIVO = 'PSV','Pasivo'
        PATRIMONIO = 'PTR','Patrimonio'
        ESTADO_RESULTADOS = 'ESR','Estado de Resultados'
        RESULTADOS_DEUDORAS = 'CRD', 'Cuentas de Resultados Deudoras'
        RESULTADOS_ACREEDORAS = 'CRA', 'Cuentas de Resultados Acreedoras'

    class Subcategoria(models.TextChoices):
        NINGUNA = 'NNG','Sin SubCategoria'
        ACTIVOCORRIENTE = 'ACTC','Activo Corriente'
        ACTIVONOCORRIENTE = 'ACTNC','Activo No Corriente'
        INVENTARIO = 'INVT','Inventario'
        PASIVOCORRIENTE = 'PSVC','Pasivo Corriente'
        PASIVONOCORRIENTE = 'PSVNC','Pasivo No Corriente'
        COSTOS = 'CTS', 'COSTOS DE VENTA'
        GASTOS_OPERACIONALES = 'GTOP', 'Gastos Operacionales'
        INGRESOS_OPERACIONALES = 'INOP', 'Ingresos Operacionales'
    
    class CuentaRatio(models.TextChoices):
        NINGUNA = 'NNG','Ninguna'
        ACTIVOCORRIENTE = 'ACTC','Activo Corriente'
        PASIVOCORRIENTE = 'PSVC','Pasivo Corriente'
        INVENTARIO = 'INVT','Inventario'
        ACTIVOSTOTALES = 'ACTV', 'Activo Totales'
        EFECTIVO = 'EFCT','Efectivo'
        VALORESCORPLAZO = 'VLRS','Valores a Corto Plazo'
        COSTODEVENTA = 'CSTDV','Costo de ventas'
        VENTASNETAS = 'VNTSN','Ventas Netas'
        COMPRAS = 'CMPRS','Compras'
        CUENTASPORPAGARCOMERCIALES = 'CNTAPP','Cuentas por pagar comerciales'
        CUENTASPORCOBRARCOMERCIALES = 'CNTAPC','Cuentas por cobrar comerciales'
    

    codigo = models.CharField(max_length=255,blank=False)
    nombre = models.CharField(max_length=255,blank=False)
    categoria = models.CharField(max_length=5,
                                 choices=Categoria.choices,
                                 default=Categoria.PASIVO)
    subcategoria = models.CharField(max_length=5,
                                    choices=Subcategoria.choices,
                                    default=Subcategoria.NINGUNA)
    cuenta_ratio = models.CharField(max_length=6,
                                      choices=CuentaRatio.choices,
                                      default=CuentaRatio.NINGUNA)
    catalogo = models.ForeignKey(Catalogo,
                                 on_delete=models.CASCADE,
                                 related_name='cuentas')
    #Managers
    objects = models.Manager()
    cuentas_activos = CuentasDebeManager()
    cuentas_pasivos = CuentasHaberManager()
    
    def __str__(self):
        return self.nombre
        
#HU-02 Modulo de transacciones

class Transaccion (models.Model):

    class TipoTransaccion(models.TextChoices):
        COMPRA = 'CMP','Compra'
        VENTA = 'VNT','Venta'
        OPERACIONAL = 'OPE', 'Operacional' #Pendiente
    
    class Naturaleza(models.TextChoices):
        CREDITO = 'CRD','Credito' #haber
        DEBITO = 'DBT','Debito' #debe

    monto = models.DecimalField(max_digits=9,decimal_places=2,blank=False)
    descripcion = models.CharField(max_length=255,blank=False)
    slug = models.SlugField(max_length=250)
    cuenta = models.ForeignKey(Cuenta,
                               on_delete=models.CASCADE,
                               related_name='transacciones') #cambiar related name a transacciones
    fecha_creacion = models.DateTimeField(default=timezone.now)
    tipo_transaccion = models.CharField(max_length=3,
                                        choices=TipoTransaccion.choices,
                                        default=TipoTransaccion.VENTA)
    naturaleza = models.CharField(max_length=3,
                                        choices=Naturaleza.choices,
                                        default=Naturaleza.CREDITO)

    #Definir Managers
    objects = models.Manager()#Manager por defecto
    
    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self) -> str:
        return self.descripcion
    
class Ratio(models.Model):
    class NombreRatio(models.TextChoices):
        PRUEBAACIDA = 'PRBCD','Prueba Ácida'
        ROTAINVENTARIO = 'RTINV','Rotación de inventarios'
    
    nombre_ratio = models.CharField(max_length=5,
                                    choices=NombreRatio.choices,
                                    default=NombreRatio.PRUEBAACIDA)
    
    valor = models.DecimalField(max_digits=9,decimal_places=2,blank=False)

    empresa = models.ForeignKey(Empresa,
                                on_delete=models.CASCADE,
                                related_name="ratios")
    def __str__(self) -> str:
        return self.nombre_ratio
    
 


    

    

