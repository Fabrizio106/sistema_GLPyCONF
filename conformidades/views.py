from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db import transaction
from django.contrib import messages
from .models import TramiteConformidad, CertificadoConformidad
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.utils import timezone
from xhtml2pdf import pisa
from datetime import timedelta
from collections import OrderedDict
import json
from datetime import date, timedelta
from django.http import JsonResponse
from .forms import CertificadoForm
from .models import TramiteConformidad, CertificadoConformidad
from glp.models import SedeConfiguracion


# ──────────────────────────────────────────
#  CONSTANTES Y HELPERS PARA EL PDF
# ──────────────────────────────────────────

CAMPO_LABELS = {
    'categoria': 'Categoría',
    'marca': 'Marca',
    'modelo': 'Modelo',
    'color': 'Color',
    'numero_vin': 'N° VIN',
    'numero_serie': 'N° Serie',
    'numero_motor': 'N° Motor',
    'anio_fabricacion': 'Año Fabricación',
    'anio_modelo': 'Año Modelo',
    'ejes': 'Ejes',
    'ruedas': 'Ruedas',
    'peso_bruto': 'Peso Bruto',
    'peso_neto': 'Peso Neto',
    'carga_util': 'Carga Útil',
    'carroceria': 'Carrocería',
    'potencia': 'Potencia',
    'combustible': 'Combustible',
    'formula_rodante': 'Fórmula Rodante',
    'cilindrada': 'Cilindrada',
    'asientos': 'Asientos',
    'pasajeros': 'Pasajeros',
    'longitud': 'Longitud',
    'altura': 'Altura',
    'ancho': 'Ancho',
    'cilindros': 'Cilindros',
}

CARROCERIAS_2008 = [
    'PICK UP', 'BARANDA', 'MINIBUS', 'MICROBÚS', 'MICROBUS',
    'OMNIBUS URBANO', 'OMNIBUS INTERURBANO', 'OMNIBUS PANORAMICO',
    'REMOLCADOR', 'GRUA', 'PANEL', 'CARGOBUS',
    'TRIMOTO PASAJEROS', 'TRIMOTO CARGA',
]

CARROCERIAS_2006 = [
    'STATION WAGON', 'HATCH BACK', 'HATCHBACK', 'SUV',
    'COUPE', 'MULTIPROPÓSITO', 'MULTIPROPOSITO', 'SEDAN',
]


def generar_norma_conformidad(tipo, campo, valor_nuevo, valor_anterior):
    campo_lower  = campo.lower()
    val_nuevo_up = str(valor_nuevo).upper().strip()

    if campo_lower == 'carroceria':
        TIPO_2008 = ['PICK UP','BARANDA','MINIBUS','MICROBÚS','MICROBUS',
                     'OMNIBUS URBANO','OMNIBUS INTERURBANO','OMNIBUS PANORAMICO',
                     'REMOLCADOR','GRUA','PANEL','CARGOBUS',
                     'TRIMOTO PASAJEROS','TRIMOTO CARGA','TRIMOTO DE PASAJEROS']
        TIPO_2006 = ['STATION WAGON','HATCH BACK','HATCHBACK','SUV',
                     'COUPE','MULTIPROPÓSITO','MULTIPROPOSITO','SEDAN',
                     'PLATAFORMA','VOLQUETE','M1']

        if tipo == 'RECTIFICACION':
            return ("(De acuerdo a la directiva RD N° 04848-2006 MTC/15 "
                    "y RD N° 10476-2008-MTC/15)")
        elif any(c in val_nuevo_up for c in [x.upper() for x in TIPO_2008]):
            return ("(Adecuación acorde a R.D. N°10476-2008-MTC/15 - NO HA EXISTIDO "
                    "MODIFICACIÓN ESTRUCTURAL EN CHASIS Y CARROCERÍA)")
        elif any(c in val_nuevo_up for c in [x.upper() for x in TIPO_2006]):
            return ("(Adecuación acorde a R.D. N°4848-2006-MTC/15 - NO HA EXISTIDO "
                    "MODIFICACIÓN ESTRUCTURAL EN CHASIS Y CARROCERÍA)")
        else:
            return ("(Adecuación a la directiva RD N° 04848-2006 MTC/15 "
                    "y RD N° 10476-2008-MTC/15)")

    if campo_lower == 'combustible':
        if 'DIESEL' in val_nuevo_up:
            return "(Adecuación a la RD N 04848-2006 MTC/15)"

    return ""


def generar_nota_conformidad(tipo, campo, valor_nuevo, valor_anterior):
    campo_lower  = campo.lower()
    val_nuevo_up = str(valor_nuevo).upper().strip()
    val_ant_up   = str(valor_anterior).upper().strip()

    if campo_lower == 'combustible':
        if 'GASOLINA' in val_nuevo_up:
            if 'GLP' in val_ant_up:
                return "EL SISTEMA BI-COMBUSTIBLE GLP HA SIDO DESMONTADO (KIT DE GLP)"
            elif 'GNV' in val_ant_up:
                return "EL VEHICULO YA NO CUENTA CON EL SISTEMA BI-COMBUSTIBLE GNV."
        if 'GLP' in val_nuevo_up and 'GLP' not in val_ant_up:
            return "EL VEHICULO CUENTA CON SISTEMA BI-COMBUSTIBLE GLP"
        if 'GNV' in val_nuevo_up and 'GNV' not in val_ant_up:
            return "EL VEHICULO MANTIENE EL SISTEMA BI-COMBUSTIBLE GNV"
        if tipo == 'RECTIFICACION':
            return "RECTIFICAR COMBUSTIBLE de acuerdo a la RD N 4848-2006-MTC/15."

    elif campo_lower == 'asientos':
        return "EL VEHÍCULO NO HA SUFRIDO MODIFICACIÓN ALGUNA CON RESPECTO AL NUMERO DE ASIENTOS."

    elif campo_lower == 'numero_motor':
        return ("EL NUEVO MOTOR ENSAMBLADO TIENE EL MISMO MODELO DEL ANTERIOR MOTOR "
                "POR LO CUAL, EL COMBUSTIBLE, CILINDRADA Y CILINDROS NO SE VEN "
                "AFECTADOS POR ESTE CAMBIO.")

    elif campo_lower == 'ruedas':
        if 'EXTRA' in val_ant_up or 'BALON' in val_ant_up:
            return "EL VEHICULO HA MODIFICADO DE RUEDAS TIPO EXTRA ANCHAS A RUEDAS TIPO CONVENCIONALES."
        else:
            return "EL VEHICULO HA MODIFICADO DE RUEDAS CONVENCIONALES A TIPO EXTRA ANCHAS (LLANTAS BALON)."

    elif campo_lower == 'categoria':
        if tipo == 'RECTIFICACION':
            return "RECTIFICAR CATEGORIA de acuerdo a la RD N 4848-2006-MTC/15."

    return ""
def render_to_pdf_conformidad(template_src, context_dict, filename="certificado"):
    template = get_template(template_src)
    html     = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}_conformidad.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error al generar PDF <pre>' + html + '</pre>')
    return response


# ──────────────────────────────────────────
#  VISTAS
# ──────────────────────────────────────────

def obtener_sedes_json():
    sedes_data = {
        str(s.id): {
            'anual_dias': s.fecha_anual,
            'inicial_dias': s.fecha_inicial
        } for s in SedeConfiguracion.objects.all()
    }
    return json.dumps(sedes_data)


@login_required
def crear_certificado_conformidad(request):
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    certificado = form.save(commit=False)
                    certificado.usuario = request.user
                    certificado.save()

                    mapa_tramites = request.POST.getlist('mapa_tramites[]')
                    for item in mapa_tramites:
                        tipo, campo = item.split('|')
                        valor_nuevo = request.POST.get(f'valor_{tipo}_{campo}')
                        if valor_nuevo:
                            TramiteConformidad.objects.create(
                                certificado=certificado,
                                tipo_nombre=tipo,
                                campo_modificado=campo,
                                valor_nuevo=valor_nuevo
                            )

                    messages.success(request, "¡Certificado y trámites registrados con éxito!", extra_tags='conformidad')
                    return redirect('crear_certificado_conformidad')
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
    else:
        form = CertificadoForm()

    return render(request, 'conformidades/conformidad_form.html', {
        'form': form,
        'sedes_json': obtener_sedes_json()
    })

def consultar_ultima_conformidad(request):
    placa = request.GET.get('placa', None)
    if not placa:
        return JsonResponse({'error': 'No se proporcionó placa'}, status=400)
    
    # Buscamos la última conformidad por fecha de emisión
    ultima = CertificadoConformidad.objects.filter(placa=placa).order_by('-fecha_emision').first()
    
    if ultima:
        fecha_expiracion = ultima.fecha_emision + timedelta(days=365)
        dias_faltantes = (fecha_expiracion - date.today()).days
        
        return JsonResponse({
            'encontrado': True,
            'placa': ultima.placa,
            'fecha_ultima': ultima.fecha_emision.strftime('%d/%m/%Y'),
            'dias_restantes': dias_faltantes if dias_faltantes > 0 else 0,
            'estado': 'VIGENTE' if dias_faltantes > 0 else 'EXPIRADO'
        })
    else:
        return JsonResponse({'encontrado': False})
    
@login_required
def historial_conformidades(request):
    certificados = (CertificadoConformidad.objects
                    .filter(usuario=request.user)
                    .order_by('-id')
                    .prefetch_related('tramites'))

    query        = request.GET.get('q')
    sede_id      = request.GET.get('sede')
    fecha_unica  = request.GET.get('fecha')
    f_inicio     = request.GET.get('inicio')
    f_fin        = request.GET.get('fin')
    tipo_tramite = request.GET.get('tipo_tramite')

    if query:
        certificados = certificados.filter(placa__icontains=query)
    if sede_id:
        certificados = certificados.filter(sede_id=sede_id)
    if fecha_unica:
        certificados = certificados.filter(fecha_emision=fecha_unica)
    elif f_inicio and f_fin:
        certificados = certificados.filter(fecha_emision__range=[f_inicio, f_fin])
    if tipo_tramite:
        certificados = certificados.filter(
            tramites__tipo_nombre=tipo_tramite
        ).distinct()

    return render(request, 'conformidades/historial_conformidades.html', {
        'certificados': certificados,
        'sedes': SedeConfiguracion.objects.all(),
        'campo_labels': CAMPO_LABELS,
    })


@login_required
def eliminar_conformidad(request, pk):
    certificado = get_object_or_404(CertificadoConformidad, pk=pk)
    if request.method == 'POST':
        certificado.delete()
        messages.success(request, "Certificado eliminado correctamente.")
    return redirect('historial_conformidades')


@login_required
def descargar_pdf_conformidad(request, pk):
    certificado = get_object_or_404(CertificadoConformidad, pk=pk)
    tramites    = list(certificado.tramites.all())

    # Agrupar trámites por tipo, manteniendo el orden de inserción
    bloques_dict = OrderedDict()
    for t in tramites:
        bloques_dict.setdefault(t.tipo_nombre, []).append(t)

    bloques = []
    notas   = []

    for tipo, items in bloques_dict.items():
        primer         = items[0]
        primer_campo   = primer.campo_modificado
        primer_val_new = primer.valor_nuevo
        valor_anterior = str(getattr(certificado, primer_campo, '') or '')

        adicionales = []
        for item in items[1:]:
            norma_ad = generar_norma_conformidad(item.tipo_nombre, item.campo_modificado,
                                                item.valor_nuevo,
                                                str(getattr(certificado, item.campo_modificado, '') or ''))
            adicionales.append({
                'label':      CAMPO_LABELS.get(item.campo_modificado, item.campo_modificado.upper()),
                'valor_nuevo': item.valor_nuevo,
                'norma':      norma_ad,
            })

        # Ajuste pesos si combustible → GASOLINA desde GLP/GNV
        if (primer_campo.lower() == 'combustible'
                and 'GASOLINA' in str(primer_val_new).upper()
                and ('GLP' in valor_anterior.upper() or 'GNV' in valor_anterior.upper())):
            if certificado.peso_neto:
                adicionales.append({
                    'label': 'PESO NETO',
                    'valor_nuevo': f'{float(certificado.peso_neto) - 30:.0f}kg',
                    'norma': '',
                })
            if certificado.carga_util:
                adicionales.append({
                    'label': 'CARGA UTIL',
                    'valor_nuevo': f'{float(certificado.carga_util) + 30:.0f}kg',
                    'norma': '',
                })

        norma_primer = generar_norma_conformidad(tipo, primer_campo, primer_val_new, valor_anterior)
        nota  = generar_nota_conformidad(tipo, primer_campo, primer_val_new, valor_anterior)
        if nota:
            notas.append(nota)

        bloques.append({
            'tipo':           tipo,
            'primer_campo':   primer_campo,
            'primer_label':   CAMPO_LABELS.get(primer_campo, primer_campo.upper()),
            'valor_anterior': valor_anterior,
            'primer_val_new': primer_val_new,
            'norma_primer':   norma_primer,
            'adicionales':    adicionales,
        })

    # Fecha del PDF = un día antes de emisión; si cae domingo → sábado
    fecha_pdf = certificado.fecha_emision or timezone.localdate()

    fecha_str = f"{fecha_pdf.day}-{fecha_pdf.month:02d}-{fecha_pdf.year}"

    # Personas o mercancías según categoría
    categoria_final = certificado.categoria or ''
    for t in tramites:
        if t.campo_modificado.lower() == 'categoria':
            categoria_final = t.valor_nuevo
            break

    tipo_transporte = 'PERSONAS' if categoria_final.upper().startswith('M') else 'MERCANCÍAS'

    context = {
        'certificado':    certificado,
        'bloques':        bloques,
        'notas':          notas,
        'fecha_str':      fecha_str,
        'tipo_transporte': tipo_transporte,
    }

    return render_to_pdf_conformidad(
        'conformidades/pdf_conformidad.html',
        context,
        filename=certificado.placa or 'certificado'
    )

@login_required
def editar_conformidad(request, pk):
    certificado = get_object_or_404(CertificadoConformidad, pk=pk)

    if request.method == 'POST':
        form = CertificadoForm(request.POST, instance=certificado)
        if form.is_valid():
            try:
                with transaction.atomic():
                    certificado.tramites.all().delete()
                    editado = form.save(commit=False)
                    editado.usuario = request.user
                    editado.fecha_emision = timezone.localdate()
                    editado.save()

                    mapa_tramites = request.POST.getlist('mapa_tramites[]')
                    tramites_guardados = 0

                    # Eliminar duplicados manteniendo orden
                    vistos = set()
                    for item in mapa_tramites:
                        try:
                            tipo, campo = item.split('|')
                            clave = f'{tipo}|{campo}'
                            if clave in vistos:
                                continue
                            vistos.add(clave)
                            valor_nuevo = request.POST.get(f'valor_{tipo}_{campo}')
                            if valor_nuevo and valor_nuevo.strip():
                                TramiteConformidad.objects.create(
                                    certificado=editado,
                                    tipo_nombre=tipo,
                                    campo_modificado=campo,
                                    valor_nuevo=valor_nuevo.strip()
                                )
                                tramites_guardados += 1
                        except ValueError:
                            continue

                    messages.success(
                        request,
                        "Certificado actualizado correctamente.",
                        extra_tags='conformidad'
                    )
                    return redirect('historial_conformidades')
            except Exception as e:
                form.add_error(None, f"Error al guardar: {e}")
    else:
        form = CertificadoForm(instance=certificado)

    import json as _json
    tramites_existentes = list(
        certificado.tramites.values('tipo_nombre', 'campo_modificado', 'valor_nuevo')
    )

    return render(request, 'conformidades/conformidad_form.html', {
        'form': form,
        'editando': True,
        'sedes_json': obtener_sedes_json(),
        'tramites_json': _json.dumps(tramites_existentes),
    })