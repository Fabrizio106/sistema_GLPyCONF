from django import forms
from .models import CertificadoGLP, SedeConfiguracion
from django.utils import timezone
from datetime import timedelta

class CertificadoGLPForm(forms.ModelForm):

    sede = forms.ModelChoiceField(
        queryset=SedeConfiguracion.objects.all(),
        empty_label="Seleccione una Sede",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = CertificadoGLP
        exclude = ['tipo_certificado', 'ciudad_glp_pdf', 'numero_certificado'] 
        
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),   
            'combustible': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccione combustible...'),
                ('BI.COMB.GLP', 'BI.COMB.GLP'),
                ('DUAL(GASOLINA/GLP)', 'DUAL(GASOLINA/GLP)'),
                ('GASOLINA', 'GASOLINA'),
                ('GNV', 'GNV'),
                # Aquí puedes agregar el resto de los combustibles de tu imagen
            ]),

            # Campos del vehículo
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'propietario': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'anio_fabricacion': forms.TextInput(attrs={'class': 'form-control'}),
            'vin_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_motor': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Medidas y Pesos
            'cilindrada': forms.TextInput(attrs={'class': 'form-control'}),
            'cilindros': forms.TextInput(attrs={'class': 'form-control'}),
            'ejes': forms.TextInput(attrs={'class': 'form-control'}),
            'ruedas': forms.TextInput(attrs={'class': 'form-control'}),
            'asientos': forms.TextInput(attrs={'class': 'form-control'}),
            'pasajeros': forms.TextInput(attrs={'class': 'form-control'}),
            'largo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'alto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peso_neto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'peso_bruto': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'carga_util': forms.NumberInput(attrs={'readonly': 'readonly', 'class': 'form-control bg-light'}),
            
            # Equipos GLP
            'reductor_marca': forms.TextInput(attrs={'class': 'form-control'}),
            'reductor_modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'reductor_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'cilindro_marca': forms.TextInput(attrs={'class': 'form-control'}),
            'cilindro_modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'cilindro_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'cilindro_capacidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cilindro_fecha_fab': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SedeConfiguracionForm(forms.ModelForm):
    class Meta:
        model = SedeConfiguracion
        fields = ['nombre_sede', 'ciudad_anual', 'fecha_anual', 'ciudad_inicial', 'fecha_inicial']
        widgets = {
            'nombre_sede': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: CERDEVA'}),
            'ciudad_anual': forms.Select(attrs={'class': 'form-select'}),
            'fecha_anual': forms.Select(attrs={'class': 'form-select'}),
            'ciudad_inicial': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicial': forms.Select(attrs={'class': 'form-select'}),
        }