from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from .forms import CertificadoForm  # Asegúrate de que este formulario use el modelo CertificadoConformidad
from .models import TramiteConformidad
from django.contrib.auth.decorators import login_required
from glp.models import SedeConfiguracion
import json

def obtener_sedes_json():
    sedes_queryset = SedeConfiguracion.objects.all()
    sedes_data = {
        str(s.id): {
            'anual_dias': s.fecha_anual,
            'inicial_dias': s.fecha_inicial
        } for s in sedes_queryset
    }
    return json.dumps(sedes_data)

@login_required
def crear_certificado_conformidad(request):
    """
    Vista procesadora para el template dinámico con Checklists y Múltiples Bloques.
    """
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        
        # Validamos el formulario principal (Secciones A y B)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # 1. Guardamos el Certificado Base sin confirmar (commit=False)
                    # Esto nos permite asignar el usuario antes de guardar en la BD
                    certificado = form.save(commit=False)
                    certificado.usuario = request.user  # Asignamos el usuario actual
                    # Ahora sí, guardamos el certificado en la base de datos
                    certificado.save()

                    # 2. Procesamos los trámites dinámicos enviados por el JS
                    # mapa_tramites[] contiene la relación "TIPO|CAMPO" (ej: RECTIFICACION|color)
                    mapa_tramites = request.POST.getlist('mapa_tramites[]')
                    
                    for item in mapa_tramites:
                        tipo, campo = item.split('|')
                        
                        # Buscamos el valor dinámico: valor_TIPO_CAMPO[]
                        # Ejemplo: valor_RECTIFICACION_color[]
                        valor_nuevo = request.POST.get(f'valor_{tipo}_{campo}')
                        if valor_nuevo:
                            # Creamos cada fila de detalle vinculada al certificado
                            TramiteConformidad.objects.create(
                                certificado=certificado,
                                tipo_nombre=tipo,
                                campo_modificado=campo,
                                valor_nuevo=valor_nuevo
                            )

                    messages.success(request, "¡Certificado y trámites registrados con éxito!")
                    return redirect('crear_certificado_conformidad')
            
            except Exception as e:
                print(f"Error en la transacción: {e}")
                form.add_error(None, f"Ocurrió un error al guardar los trámites: {e}")
    else:
        # Petición GET: Formulario limpio
        form = CertificadoForm()

    return render(request, 'conformidades/conformidad_form.html', {
        'form': form,
        'sedes_json': obtener_sedes_json()
    })