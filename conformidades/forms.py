from django import forms
from django.forms import inlineformset_factory
from .models import CertificadoConformidad, TramiteConformidad

class CertificadoForm(forms.ModelForm):
    class Meta:
        model = CertificadoConformidad
        # Incluimos todos los campos del modelo
        fields = '__all__'
        # Excluimos la fecha de registro porque se pone sola
        exclude = ['fecha_registro']
        
        # Agregamos clases de Bootstrap para que se vea bien
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'}) 
            for field in [
                'numero_vin', 'placa', 'categoria', 'marca', 'modelo', 
                'color', 'numero_serie', 'numero_motor', 'carroceria', 
                'potencia', 'formula_rodante', 'combustible', 'asientos', 
                'pasajeros', 'ruedas', 'ejes', 'cilindros', 'cilindrada',
                'anio_fabricacion', 'anio_modelo', 'version'
            ]
        }
        # Los campos numéricos necesitan su propio widget
        widgets.update({
            'longitud': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'carga_util': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        })

class TramiteForm(forms.ModelForm):
    class Meta:
        model = TramiteConformidad
        fields = ['tipo_nombre', 'campo_modificado', 'valor_nuevo']
        widgets = {
            'tipo_nombre': forms.Select(attrs={'class': 'form-select'}),
            'campo_modificado': forms.Select(attrs={'class': 'form-select'}), # Cambiado a Select para tu JS
            'valor_nuevo': forms.TextInput(attrs={'class': 'form-control'}),
        }

# ESTE ES EL MOTOR DINÁMICO
# Crea un conjunto de formularios de Trámites vinculados a un Certificado
TramiteFormSet = inlineformset_factory(
    CertificadoConformidad, 
    TramiteConformidad, 
    form=TramiteForm,
    extra=1,            # Número de formularios vacíos que aparecen al inicio
    can_delete=True     # Permite eliminar trámites añadidos
)