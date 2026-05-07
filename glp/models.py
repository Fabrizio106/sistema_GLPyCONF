from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

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

class CertificadoGLP(models.Model):
    # 1. Datos del Certificado (Estos campos ya no se llenan a mano, se calculan solos)
    numero_certificado = models.CharField(max_length=20, unique=True, verbose_name="N° de Certificado")
    tipo_certificado = models.CharField(max_length=10, blank=True, verbose_name="Tipo de Certificado")
    fecha_emision = models.DateField(blank=True, null=True)
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
    
    # Este campo es el "gatillo" para saber si es Inicial o Anual
    combustible = models.CharField(max_length=50, verbose_name="Combustible")
    
    # 3. Especificaciones Técnicas
    cilindrada = models.CharField(max_length=20, verbose_name="Cilindrada")
    cilindros = models.CharField(max_length=10, verbose_name="Cilindros")
    ejes = models.CharField(max_length=10, verbose_name="N° Ejes")
    ruedas = models.CharField(max_length=10, verbose_name="N° Ruedas")
    asientos = models.CharField(max_length=10, verbose_name="Asientos")
    pasajeros = models.CharField(max_length=10, verbose_name="Pasajeros")
    
    # Dimensiones y Pesos
    largo = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Longitud (m)", null=True, blank=True)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Ancho (m)", null=True, blank=True)
    alto = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Altura (m)", null=True, blank=True)
    peso_neto = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Peso Neto (kg)")
    peso_bruto = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Peso Bruto (kg)")
    carga_util = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Carga Útil (kg)")

    # 4. Datos del Equipo GLP
    reductor_marca = models.CharField(max_length=50, verbose_name="Marca Reductor")
    reductor_modelo = models.CharField(max_length=50, verbose_name="Modelo Reductor")
    reductor_serie = models.CharField(max_length=50, verbose_name="Serie Reductor")
    
    cilindro_marca = models.CharField(max_length=50, verbose_name="Marca Cilindro")
    cilindro_modelo = models.CharField(max_length=50, verbose_name="Modelo Cilindro")
    cilindro_serie = models.CharField(max_length=50, verbose_name="Serie Cilindro")
    cilindro_capacidad = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Capacidad (L)")
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
    def fecha_emision_es(self):
        if not self.fecha_emision:
            return ""
        meses = ("enero", "febrero", "marzo", "abril", "mayo", "junio", 
                "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre")
        dias = ("lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo")
        
        dia_nombre = dias[self.fecha_emision.weekday()]
        mes_nombre = meses[self.fecha_emision.month - 1]
        
        return f"{dia_nombre} {self.fecha_emision.day} de {mes_nombre} de {self.fecha_emision.year}"
    
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
        
        # sede y ciudad para el PDF
        config = self.sede 
        if self.tipo_certificado == 'ANUAL':
            self.ciudad_glp_pdf = config.ciudad_anual
            regla_fecha = config.fecha_anual
        else:
            self.ciudad_glp_pdf = config.ciudad_inicial
            regla_fecha = config.fecha_inicial
        
        if not self.fecha_emision:
            hoy = timezone.now().date()
            if regla_fecha == 'MISMO':
                self.fecha_emision = hoy
            elif regla_fecha == 'ANTES':
                self.fecha_emision = hoy - timedelta(days=1)
            elif regla_fecha == 'ANTES_2':
                self.fecha_emision = hoy - timedelta(days=2)
            # Si el cálculo resulta en Domingo de retro al sabad
        if self.fecha_emision and self.fecha_emision.weekday() == 6:
            self.fecha_emision = self.fecha_emision - timedelta(days=1)   

        if self.fecha_emision:
            self.fecha_vencimiento = self.fecha_emision + timedelta(days=365)

        super().save(*args, **kwargs)