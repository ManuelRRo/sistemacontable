from django import forms
from .models import Catalogo,Empresa,Cuenta,Transaccion


class CatalagoForm(forms.ModelForm):

    class Meta:
        model = Catalogo
        fields = ['archivo']

class EmpresaForm(forms.Form):
    nombre_empresa = forms.CharField(max_length=100)
    sectores = forms.ChoiceField(choices=Empresa.Sector.choices)

class ActivoCorrienteForm(forms.Form):
    user = None
    cuentasUsuario = None
    request_ = None
    activo_corriente = forms.ModelChoiceField(queryset=cuentasUsuario)
    pasivo_corriente = forms.ModelChoiceField(queryset=cuentasUsuario)
    inventario = forms.ModelChoiceField(queryset=cuentasUsuario)
    activos_totales = forms.ModelChoiceField(queryset=cuentasUsuario)
    efectivo = forms.ModelChoiceField(queryset=cuentasUsuario)
    valores_a_corto_plazo = forms.ModelChoiceField(queryset=cuentasUsuario)
    costo_de_venta = forms.ModelChoiceField(queryset=cuentasUsuario)
    ventas_netas = forms.ModelChoiceField(queryset=cuentasUsuario)
    compras = forms.ModelChoiceField(queryset=cuentasUsuario)
    cuentas_por_pagar_comerciales = forms.ModelChoiceField(queryset=cuentasUsuario)
    cuentas_por_cobrar_comerciales = forms.ModelChoiceField(queryset=cuentasUsuario)

    def __init__(self,request_, user=None, *args, **kwargs):
        self.user = user
        self.request_ = request_
        self.lista = []
        try:
            if self.user is not None:
                self.cuentasUsuario = self.user.propietario.empresa.catalogo_empresa.cuentas.all()
            else:
                for cuenta, codigo_ratio in request_.POST.items():
                    if cuenta != "csrfmiddlewaretoken":
                            self.lista.append(
                                 Cuenta.objects.get(pk=codigo_ratio)
                                 )
        except Exception as e:
            error_message = f"Se produjo una excepción: {str(e)}"
            print(error_message)
            print("Usuario igual None 1")

        super(ActivoCorrienteForm, self).__init__(*args, **kwargs)
        
        try:
            if self.user is not None:
                for field_name, field in self.fields.items():
                    field.queryset = self.cuentasUsuario
            else:
                self.cuentasUsuario = self.request_.user.propietario.empresa.catalogo_empresa.cuentas.all()
                for (field_name, field), cuenta in zip(self.fields.items(), self.lista):
                    field.queryset = self.cuentasUsuario
                    field.initial = cuenta
                    print("cAMPO INITIAL ", field.initial)
                
        except Exception as e:
            error_message = f"Se produjo una excepción: {str(e)}"
            print(error_message)
            print("Usuario igual None 2")
            print("USER ",self.user," request ",self.request_)
        #cambiar labels
        #self.fields['activo_corriente'].label = "Activo Corllllriente"
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'btn btn-primary'})

        
class UpdateTransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['cuenta', 'monto']

        widgets = {
            'cuenta': forms.Select(attrs={'class': 'form-control d-none'}),
            'monto': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UpdateCuentaForm(forms.Form):
        nombre_empresa = forms.CharField(max_length=100)
        sectores = forms.ChoiceField(choices=Empresa.Sector.choices)