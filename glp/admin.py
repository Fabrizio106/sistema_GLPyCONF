from django.contrib import admin
from .models import CertificadoGLP, SedeConfiguracion
from conformidades.models import CertificadoConformidad, TramiteConformidad

@admin.register(CertificadoGLP)
class CertificadoGLPAdmin(admin.ModelAdmin):
    # Columnas que se verán en la tabla resumen
    list_display = ('numero_certificado', 'placa', 'tipo_certificado', 'fecha_emision', 'sede')
    # Barra de búsqueda
    search_fields = ('numero_certificado', 'placa', 'propietario')
    # Filtros laterales
    list_filter = ('tipo_certificado', 'sede')

@admin.register(SedeConfiguracion)
class SedeConfiguracionAdmin(admin.ModelAdmin):
    list_display = ('nombre_sede', 'ciudad_anual', 'ciudad_inicial')

# Configuración para ver los Trámites dentro del Certificado
class TramiteInline(admin.TabularInline):
    model = TramiteConformidad
    extra = 1  # Muestra una fila vacía para agregar rápido
    fields = ('tipo_nombre', 'campo_modificado', 'valor_nuevo')

@admin.register(CertificadoConformidad)
class CertificadoAdmin(admin.ModelAdmin):
    # Columnas para la tabla principal
    list_display = ('numero_certificado','placa', 'marca', 'modelo', 'anio_fabricacion', 'carga_util')
    # Buscador por placa o VIN
    search_fields = ('numero_certificado','placa', 'numero_vin', 'numero_serie')
    # Filtro lateral
    list_filter = ('marca', 'anio_fabricacion')
    # Integración de los trámites
    inlines = [TramiteInline]

@admin.register(TramiteConformidad)
class TramiteAdmin(admin.ModelAdmin):
    list_display = ('certificado', 'tipo_nombre', 'campo_modificado', 'valor_nuevo')
    list_filter = ('tipo_nombre',)