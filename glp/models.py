from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class SedeConfiguracion(models.Model):
    OPCIONES_FECHA = [
        ('MISMO', 'Mismo día'),
        ('ANTES', 'Un día antes'),
        ('ANTES_2', '2 días antes'),
    ]

    OPCIONES_CIUDAD = [
        ('CHICLAYO', 'Chiclayo'),
        ('CHIMBOTE', 'Chimbote'),
        ('LIMA', 'Lima'),
    ]

    nombre_sede = models.CharField(max_length=100, unique=True, verbose_name="Nombre de la Sede")
    
    ciudad_anual = models.CharField(max_length=20, choices=OPCIONES_CIUDAD)
    fecha_anual = models.CharField(max_length=10, choices=OPCIONES_FECHA)
    
    ciudad_inicial = models.CharField(max_length=20, choices=OPCIONES_CIUDAD)
    fecha_inicial = models.CharField(max_length=10, choices=OPCIONES_FECHA)

    def __str__(self):
        return self.nombre_sede

COMBUSTIBLE_CHOICES = [
    ('ANUAL (GLP y otros)', (
        ('BI.COMB.GLP', 'BI.COMB.GLP'),
        ('BI-COMBUSTIBLE GLP', 'BI-COMBUSTIBLE GLP'),
        ('BI COMB./GLP', 'BI COMB./GLP'),
        ('BI.COMBUS.GLP', 'BI.COMBUS.GLP'),
        ('BI.COMBUST.GLP', 'BI.COMBUST.GLP'),
        ('DUAL(GASOLINA/GLP)', 'DUAL(GASOLINA/GLP)'),
        ('GAS', 'GAS'),
        ('GAS NATURAL COMPR', 'GAS NATURAL COMPR'),
        ('GAS-GASOLINA', 'GAS-GASOLINA'),
        ('GASOL/DUAL', 'GASOL/DUAL'),
        ('GASOL/GLP', 'GASOL/GLP'),
        ('GAS-GLP', 'GAS-GLP'),
        ('GASOLINA-GAS', 'GASOLINA-GAS'),
        ('GASOLINA/GLP', 'GASOLINA/GLP'),
        ('GASOLINA/GNC', 'GASOLINA/GNC'),
        ('GLP', 'GLP'),
        ('GSL/GASP', 'GSL/GASP'),
    )),
    ('INICIAL (GNV y otros)', (
        ('BI COMB.-GNV', 'BI COMB.-GNV'),
        ('BI COMBUSTIBLE GNV', 'BI COMBUSTIBLE GNV'),
        ('BI-GNV', 'BI-GNV'),
        ('DUAL GNV', 'DUAL GNV'),
        ('GASOL/GNV', 'GASOL/GNV'),
        ('GASOLINA/GNV', 'GASOLINA/GNV'),
        ('GNV', 'GNV'),
        ('GASOLINA', 'GASOLINA'),
        ('GASOLINA PREMIUM SIN PLOMO', 'GASOLINA PREMIUM SIN PLOMO'),
    )),
]

class CertificadoGLP(models.Model):
    # 1. Datos del Certificado
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Certificador", null=True, blank=True)
    numero_certificado = models.CharField(max_length=20, unique=True, verbose_name="N° de Certificado")
    tipo_certificado = models.CharField(max_length=10, blank=True, verbose_name="Tipo de Certificado")
    fecha_emision = models.DateField(blank=True, null=True, verbose_name="Fecha de Emisión (Real)")
    fecha_certificacion = models.DateField(blank=True, null=True, verbose_name="Fecha del Documento") 
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Registro en Sistema")
    sede = models.ForeignKey(SedeConfiguracion, on_delete=models.PROTECT, verbose_name="Sede")
    ciudad_glp_pdf = models.CharField(max_length=100, blank=True, editable=False)

    # 2. Datos del Vehículo
    placa = models.CharField(max_length=10, verbose_name="Placa")
    propietario = models.CharField(max_length=200, verbose_name="Propietario")
    categoria = models.CharField(max_length=20, verbose_name="Categoría")
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=100, verbose_name="Modelo")
    version = models.CharField(max_length=100, blank=True, null=True, verbose_name="Versión")
    anio_fabricacion = models.CharField(max_length=4, verbose_name="Año de Fab.")
    vin_serie = models.CharField(max_length=50, verbose_name="VIN / N° de serie")
    numero_motor = models.CharField(max_length=50, verbose_name="N° Motor")
    
    combustible = models.CharField(max_length=50, verbose_name="Combustible", choices=COMBUSTIBLE_CHOICES)
    
    # 3. Especificaciones Técnicas
    cilindrada = models.CharField(max_length=20, verbose_name="Cilindrada")
    cilindros = models.CharField(max_length=10, verbose_name="Cilindros")
    ejes = models.CharField(max_length=10, verbose_name="N° Ejes")
    ruedas = models.CharField(max_length=10, verbose_name="N° Ruedas")
    asientos = models.CharField(max_length=10, verbose_name="Asientos")
    pasajeros = models.CharField(max_length=10, verbose_name="Pasajeros")
    
    # Dimensiones y Pesos
    largo = models.CharField(max_length=20, verbose_name="Largo (m)", blank=True, null=True)
    ancho = models.CharField(max_length=20, verbose_name="Ancho (m)", blank=True, null=True)
    alto = models.CharField(max_length=20, verbose_name="Altura (m)", blank=True, null=True)
    peso_neto = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Peso Neto (kg)")
    peso_bruto = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Peso Bruto (kg)")
    carga_util = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Carga Útil (kg)")

    # 4. Datos del Equipo GLP
    reductor_marca = models.CharField(max_length=50, verbose_name="Marca Reductor")
    reductor_modelo = models.CharField(max_length=50, verbose_name="Modelo Reductor")
    reductor_serie = models.CharField(max_length=50, verbose_name="Serie Reductor")
    
    cilindro_marca = models.CharField(max_length=50, verbose_name="Marca Cilindro")
    cilindro_modelo = models.CharField(max_length=50, verbose_name="Modelo Cilindro")
    cilindro_serie = models.CharField(max_length=50, verbose_name="Serie Cilindro")
    cilindro_capacidad = models.DecimalField(max_digits=8, decimal_places=4, verbose_name="Capacidad (L)")
    cilindro_fecha_fab = models.CharField(max_length=20, verbose_name="Fecha Fabricación Cilindro")

    fecha_vencimiento = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "Certificado GLP"
        verbose_name_plural = "Certificados GLP"

    def __str__(self):
        return f"{self.numero_certificado} - {self.placa} ({self.tipo_certificado})"
    
    def clean(self):
        if not self.pk and not self.numero_certificado:
            ultimo = CertificadoGLP.objects.filter(
                numero_certificado__gte="10000"
            ).order_by('numero_certificado').last()
        
            if ultimo and ultimo.numero_certificado.isdigit():
                self.numero_certificado = str(int(ultimo.numero_certificado) + 1)
            else:
                self.numero_certificado = "10001"

        #  para que el bruto sea mayor a mi neto 
        if self.peso_bruto and self.peso_neto:
            if self.peso_bruto <= self.peso_neto:
                raise ValidationError({'peso_bruto': "El Peso Bruto debe ser mayor al Peso Neto."})
            self.carga_util = float(self.peso_bruto) - float(self.peso_neto)
    
    @property
    def fecha_certificacion_es(self):
        if not self.fecha_certificacion:
            return ""
        meses = ("enero", "febrero", "marzo", "abril", "mayo", "junio", 
                "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        dias = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
        
        dia_nombre = dias[self.fecha_certificacion.weekday()]
        mes_nombre = meses[self.fecha_certificacion.month - 1]
        
        return f"{dia_nombre} {self.fecha_certificacion.day} de {mes_nombre} de {self.fecha_certificacion.year}"
    
    def save(self, *args, **kwargs):
        self.full_clean() 
        # segun el combustible se sabe si es anal o inciial
        combustibles_inicial = [
            'BI COMB.-GNV', 'BI COMBUSTIBLE GNV', 'BI-GNV', 'DUAL GNV',
            'GASOL/GNV', 'GASOLINA/GNV', 'GNV', 'GASOLINA', 'GASOLINA PREMIUM SIN PLOMO'
        ]
        
        if self.combustible in combustibles_inicial:
            self.tipo_certificado = 'INICIAL'
        else:
            self.tipo_certificado = 'ANUAL' 
        
        
        self.fecha_emision = timezone.localdate()
        
        # sede y ciudad para el PDF
        config = self.sede 
        if self.tipo_certificado == 'ANUAL':
            self.ciudad_glp_pdf = config.ciudad_anual
            regla_fecha = config.fecha_anual
        else:
            self.ciudad_glp_pdf = config.ciudad_inicial
            regla_fecha = config.fecha_inicial
        
        if regla_fecha == 'MISMO':
            self.fecha_certificacion = self.fecha_emision
        elif regla_fecha == 'ANTES':
            self.fecha_certificacion = self.fecha_emision - timedelta(days=1)
        elif regla_fecha == 'ANTES_2':
            self.fecha_certificacion = self.fecha_emision - timedelta(days=2)
        else:
            self.fecha_certificacion = self.fecha_emision
        

            # Si el cálculo resulta en Domingo de retro al sabad
        if self.fecha_certificacion and self.fecha_certificacion.weekday() == 6:
            self.fecha_certificacion = self.fecha_certificacion - timedelta(days=1)

        self.fecha_vencimiento = self.fecha_emision + timedelta(days=365)

        super().save(*args, **kwargs)