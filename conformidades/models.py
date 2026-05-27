from django.db import models
from glp.models import SedeConfiguracion
from django.conf import settings

class CertificadoConformidad(models.Model):
    """
    Modelo Base: Representa el vehículo y los datos originales del certificado.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        verbose_name='Certificador'
    )
    
    sede = models.ForeignKey(SedeConfiguracion, on_delete=models.PROTECT, verbose_name="Sede")
    propietario = models.CharField(max_length=300, blank=True, null=True, verbose_name="Titular / Propietario")
    fecha_emision = models.DateField(blank=True, null=True, verbose_name="Fecha de Emisión (Real)")
    numero_certificado = models.CharField(max_length=20, unique=True,null=True,blank=True, verbose_name="N° de Certificado")
    # Identificación Básica
    numero_vin = models.CharField(max_length=17, unique=True, verbose_name="Número VIN")
    placa = models.CharField(max_length=100, verbose_name="Placa")
    categoria = models.CharField(max_length=20, blank=True, null=True, verbose_name="Categoría")
    marca = models.CharField(max_length=50, blank=True, null=True, verbose_name="Marca")
    modelo = models.CharField(max_length=100, blank=True, null=True, verbose_name="Modelo")
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color")
    
    # Series y Motor
    numero_serie = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Serie")
    numero_motor = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Motor")
    carroceria = models.CharField(max_length=100, blank=True, null=True, verbose_name="Carrocería")
    potencia = models.CharField(max_length=50, blank=True, null=True, verbose_name="Potencia")
    formula_rodante = models.CharField(max_length=20, blank=True, null=True, verbose_name="Fórmula Rodante")
    combustible = models.CharField(max_length=50, blank=True, null=True, verbose_name="Combustible")
    
    # Capacidades
    asientos = models.CharField(max_length=10, blank=True, null=True, verbose_name="Asientos")
    pasajeros = models.CharField(max_length=10, blank=True, null=True, verbose_name="Pasajeros")
    ruedas = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ruedas")
    ejes = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ejes")
    cilindros = models.CharField(max_length=10, blank=True, null=True, verbose_name="Cilindros")
    
    # Medidas (DecimalField para precisión técnica)
    longitud = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Longitud (m)")
    altura = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Altura (m)")
    ancho = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name="Ancho (m)")
    cilindrada = models.CharField(max_length=20, blank=True, null=True, verbose_name="Cilindrada")
    
    # Pesos
    peso_bruto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Peso Bruto (kg)")
    peso_neto = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Peso Neto (kg)")
    carga_util = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Carga Útil (kg)")
    
    # Fabricación
    anio_fabricacion = models.CharField(max_length=4, blank=True, null=True, verbose_name="Año Fab.")
    anio_modelo = models.CharField(max_length=4, blank=True, null=True, verbose_name="Año Modelo")
    version = models.CharField(max_length=100, blank=True, null=True, verbose_name="Versión")
    
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Certificado de Conformidad"
        verbose_name_plural = "Certificados de Conformidad"

    def __str__(self):
        return f"{self.placa} - {self.numero_vin}"
    
    def clean(self):
        if not self.pk and not self.numero_certificado:
            from django.utils import timezone
            year_suffix = str(timezone.now().year)[-2:]  # "26" para 2026
            ultimo = CertificadoConformidad.objects.filter(
                numero_certificado__endswith=f"-{year_suffix}"
            ).order_by('numero_certificado').last()
            if ultimo:
                try:
                    seq = int(ultimo.numero_certificado.split('-')[0]) + 1
                except (IndexError, ValueError):
                    seq = 1
            else:
                seq = 1
            self.numero_certificado = f"{seq:07d}-{year_suffix}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class TramiteConformidad(models.Model):
    """
    Modelo Detalle: Representa los cambios dinámicos realizados a un certificado.
    """
    TIPO_TRAMITE_CHOICES = [
        ('RECTIFICACION', 'Rectificación'),
        ('ADECUACION', 'Adecuación'),
        ('INCORPORACION', 'Incorporación'),
        ('MODIFICACION', 'Modificación'),
    ]

    certificado = models.ForeignKey(
        CertificadoConformidad, 
        on_delete=models.CASCADE, 
        related_name='tramites',
        verbose_name="Certificado Asociado"
    )
    
    tipo_nombre = models.CharField(
        max_length=50, 
        choices=TIPO_TRAMITE_CHOICES, 
        verbose_name="Tipo de Trámite"
    )
    
    campo_modificado = models.CharField(
        max_length=50, 
        verbose_name="Dato a cambiar"
    )
    
    valor_nuevo = models.CharField(
        max_length=255, 
        verbose_name="Nuevo Valor"
    )
    
    fecha_tramite = models.DateField(auto_now_add=True, verbose_name="Fecha del Trámite")

    class Meta:
        verbose_name = "Detalle de Trámite"
        verbose_name_plural = "Detalles de Trámites"

    def __str__(self):
        return f"{self.tipo_nombre}: {self.campo_modificado} -> {self.valor_nuevo}"