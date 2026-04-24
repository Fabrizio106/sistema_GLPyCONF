from django.db import models
from django.utils import timezone
from datetime import timedelta

class CertificadoGLP(models.Model):
    # 1. Datos del Certificado (Estos campos ya no se llenan a mano, se calculan solos)
    numero_certificado = models.CharField(max_length=20, unique=True, verbose_name="N° de Certificado")
    tipo_certificado = models.CharField(max_length=10, blank=True, verbose_name="Tipo de Certificado")
    fecha_emision = models.DateField(blank=True, null=True, verbose_name="Fecha de Emisión")
    sede = models.CharField(max_length=100, verbose_name="Sede") 

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

    class Meta:
        verbose_name = "Certificado GLP"
        verbose_name_plural = "Certificados GLP"

    def __str__(self):
        return f"{self.numero_certificado} - {self.placa} ({self.tipo_certificado})"

    # ====== AQUÍ EMPIEZA LA MAGIA DE LA AUTOMATIZACIÓN ======
    def save(self, *args, **kwargs):
        # 1. Regla de Combustible -> Tipo de Certificado
        combustibles_inicial = [
            'BI COMB.-GNV', 'BI COMBUSTIBLE GNV', 'BI-GNV', 'DUAL GNV',
            'GASOL/GNV', 'GASOLINA/GNV', 'GNV', 'GASOLINA', 'GASOLINA PREMIUM SIN PLOMO'
        ]
        
        if self.combustible in combustibles_inicial:
            self.tipo_certificado = 'INICIAL'
        else:
            self.tipo_certificado = 'ANUAL' # Por defecto todos los demás (GLP, etc.) son anuales.

        # 2. Regla de Sede -> Cálculo de Fecha
        # Si la fecha no ha sido forzada manualmente, la calculamos:
        if not self.fecha_emision:
            hoy = timezone.now().date()
            sede_upper = self.sede.upper()
            
            # Sedes que siempre son el MISMO DIA
            sedes_mismo_dia = ['POTENZA', 'SAN JUAN DE LURIGANCHO', 'CASMA']
            
            # Sedes que siempre son DOS DIAS ANTES
            sedes_dos_dias = ['ACURA GLP']
            
            # Casos especiales (Ej: CERDEVA es Mismo día para anual, pero un día antes para inicial)
            if sede_upper == 'CERDEVA':
                if self.tipo_certificado == 'ANUAL':
                    self.fecha_emision = hoy
                else:
                    self.fecha_emision = hoy - timedelta(days=1)
            
            elif sede_upper in sedes_mismo_dia:
                self.fecha_emision = hoy
                
            elif sede_upper in sedes_dos_dias:
                self.fecha_emision = hoy - timedelta(days=2)
                
            else:
                # REGLA GENERAL POR DEFECTO: La mayoría (Revi Chiclayo, Chepen, etc.) son UN DIA ANTES
                self.fecha_emision = hoy - timedelta(days=1)

        # Finalmente, mandamos a guardar a la base de datos
        super().save(*args, **kwargs)