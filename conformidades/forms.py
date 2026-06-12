from django import forms
from django.forms import inlineformset_factory
from .models import CertificadoConformidad, TramiteConformidad
from glp.models import SedeConfiguracion
from datetime import date, timedelta

class CertificadoForm(forms.ModelForm):
    
    nota_modificacion = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3, 
            'class': 'form-control', 
            'placeholder': 'Escriba una nota sobre la modificación de motor/combustible...'
        }),
        required=False,
        label="Nota"
    )
    
    sede = forms.ModelChoiceField(
        queryset=SedeConfiguracion.objects.all(),
        empty_label="Seleccione una Sede",
        widget=forms.Select(attrs={'class': 'form-select'})
        )
    
    def __init__(self, *args, **kwargs):
        super(CertificadoForm, self).__init__(*args, **kwargs)
        # LÓGICA DE FECHA AUTOMÁTICA: 
        # Si el formulario es nuevo (no tiene instancia grabada), ponemos hoy.
        if not self.instance.pk:
            self.fields['fecha_emision'].initial = date.today()- timedelta(days=1)
        
        # Mostrar enteros al editar
        if self.instance and self.instance.pk:
            if self.instance.peso_bruto is not None:
                self.initial['peso_bruto'] = int(self.instance.peso_bruto)

            if self.instance.peso_neto is not None:
                self.initial['peso_neto'] = int(self.instance.peso_neto)

            if self.instance.carga_util is not None:
                self.initial['carga_util'] = int(self.instance.carga_util)
    
    class Meta:
        model = CertificadoConformidad
        # Incluimos todos los campos del modelo
        fields = '__all__'
        # Excluimos la fecha de registro porque se pone sola
        exclude = ['fecha_registro', 'numero_certificado']
        
        # Agregamos clases de Bootstrap para que se vea bien
        widgets = {
            field: forms.TextInput(attrs={'class': 'form-control'}) 
            for field in [
                'numero_vin', 'categoria', 'marca', 'modelo', 
                'color', 'numero_serie', 'numero_motor', 'carroceria', 
                'potencia', 'formula_rodante', 'combustible', 'asientos', 
                'pasajeros', 'ruedas', 'ejes', 'cilindros', 'cilindrada',
                'anio_fabricacion', 'anio_modelo', 'version'
            ]
            
        }
        # Los campos numéricos necesitan su propio widget
        widgets.update({
            'placa': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '10',
                'pattern': '[A-Za-z0-9-]{1,10}',  
                'title': 'La placa debe tener como máximo 10 caracteres alfanuméricos',
                'style': 'text-transform: uppercase;'
            }),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'longitud': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00001'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'carga_util': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control bg-light'}),
            'propietario': forms.TextInput(attrs={'class': 'form-control'}),
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