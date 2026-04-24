from django.shortcuts import render, redirect
from .forms import CertificadoGLPForm
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import CertificadoGLP
from django.shortcuts import get_object_or_404


def crear_certificado_glp(request):
    if request.method == 'POST':
        form = CertificadoGLPForm(request.POST)
        if form.is_valid():
            form.save() # Guarda en la base de datos
            return redirect('crear_glp') # Recarga la página limpia
    else:
        form = CertificadoGLPForm()

    return render(request, 'glp/formulario_glp.html', {'form': form})
# Create your views here.

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
    # Buscamos el certificado específico por su ID (pk)
    certificado = get_object_or_404(CertificadoGLP, pk=pk)
    # Reutilizamos la función que ya tenemos para generar el PDF
    return render_to_pdf('glp/pdf_certificado.html', {'certificado': certificado}, filename=certificado.placa)