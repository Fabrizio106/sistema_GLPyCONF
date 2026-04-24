from django import forms
from .models import CertificadoGLP

class CertificadoGLPForm(forms.ModelForm):
    class Meta:
        model = CertificadoGLP
        # Excluimos tipo_certificado porque lo calculamos nosotros
        exclude = ['tipo_certificado'] 
        
        # Le damos estilo a todos los campos para que se vean bien con Bootstrap
        widgets = {
            'numero_certificado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 00016391'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            
            # Convertimos la sede y el combustible en menús desplegables (select)
            'sede': forms.Select(attrs={'class': 'form-select'}, choices=[
                ('', 'Seleccione una sede...'),
                ('REVI CHICLAYO', 'REVI CHICLAYO'),
                ('POTENZA', 'POTENZA'),
                ('ACURA GLP', 'ACURA GLP'),
                ('CERDEVA', 'CERDEVA'),
                # Aquí puedes agregar el resto de las sedes de tu PDF
            ]),
            
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
            'carga_util': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),

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