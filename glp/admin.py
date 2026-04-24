from django.contrib import admin
from .models import CertificadoGLP

@admin.register(CertificadoGLP)
class CertificadoGLPAdmin(admin.ModelAdmin):
    # Columnas que se verán en la tabla resumen
    list_display = ('numero_certificado', 'placa', 'tipo_certificado', 'fecha_emision', 'sede')
    # Barra de búsqueda
    search_fields = ('numero_certificado', 'placa', 'propietario')
    # Filtros laterales
    list_filter = ('tipo_certificado', 'sede')
