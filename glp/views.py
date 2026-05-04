from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import CertificadoGLP, SedeConfiguracion
from .forms import SedeConfiguracionForm, CertificadoGLPForm
from datetime import timedelta
from django.utils import timezone
import json
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

def registrar_certificado_glp(request):
    if request.method == 'POST':
        form = CertificadoGLPForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "¡Certificado registrado con éxito!")
            return redirect('registrar_glp') 
    else:
        form = CertificadoGLPForm()

    # --- LÓGICA PARA PASAR LAS SEDES AL JAVASCRIPT ---
    sedes_queryset = SedeConfiguracion.objects.all()

    sedes_data = {
        str(s.id): {
            'anual_dias': s.fecha_anual,
            'inicial_dias': s.fecha_inicial
        } for s in sedes_queryset
    }

    return render(request, 'glp/formulario_glp.html', {
        'form': form,
        'sedes_json': json.dumps(sedes_data)
    })


def render_to_pdf(template_src, context_dict={}, filename="documento"):
    template = get_template(template_src)
    # Esta línea es la que cambia {{ certificado.placa }} por "ABC-123"
    html = template.render(context_dict) 
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    
    # pisa.CreatePDF recibe el html YA TRADUCIDO
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Error <pre>' + html + '</pre>')
    return response

def historial_glp(request):
    # Buscamos todos los certificados y los ordenamos por ID descendente
    certificados = CertificadoGLP.objects.all().order_by('-id')
    
    # Si el usuario busca por placa en el buscador que pondremos:
    query = request.GET.get('q')
    if query:
        certificados = certificados.filter(placa__icontains=query)
        
    return render(request, 'glp/historial_glp.html', {'certificados': certificados})

def descargar_pdf_glp(request, pk):
    certificado = get_object_or_404(CertificadoGLP, pk=pk)
    return render_to_pdf('glp/pdf_certificado.html', {'certificado': certificado}, filename=certificado.placa)


@staff_member_required
def gestion_sedes(request, pk=None):
    # Si hay un PK, estamos editando
    sede_instancia = get_object_or_404(SedeConfiguracion, pk=pk) if pk else None
    
    if request.method == 'POST':
        form = SedeConfiguracionForm(request.POST, instance=sede_instancia)
        if form.is_valid():
            form.save()
            return redirect('gestion_sedes')
    else:
        form = SedeConfiguracionForm(instance=sede_instancia)

    sedes = SedeConfiguracion.objects.all()
    return render(request, 'glp/sede_configuracion.html', {
        'form': form,
        'sedes': sedes,
        'editando': sede_instancia
    })

def eliminar_sede(request, pk):
    sede = get_object_or_404(SedeConfiguracion, pk=pk)
    sede.delete()
    return redirect('gestion_sedes')