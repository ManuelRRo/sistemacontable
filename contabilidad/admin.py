from django.contrib import admin

from .models import Cuenta,Transaccion,Empresa,Catalogo,Propietario,Ratio

@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ['codigo','nombre','categoria','cuenta_ratio','catalogo']

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ['cuenta','descripcion','monto']

@admin.register(Catalogo)
class CatalogoAdmin(admin.ModelAdmin):
    pass

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    pass

@admin.register(Propietario)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Ratio)
class RatioAdmin(admin.ModelAdmin):
    list_display = ['nombre_ratio','empresa','valor']