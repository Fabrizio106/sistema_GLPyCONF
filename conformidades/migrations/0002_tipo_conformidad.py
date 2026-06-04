# conformidades/migrations/0002_tramite_dinamico.py
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        ('conformidades', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TramiteConformidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                # LA LLAVE: Relaciona muchos trámites a un solo certificado
                ('certificado', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, 
                    to='conformidades.CertificadoConformidad',
                    related_name='tramites' # Esto permite hacer certificado.tramites.all()
                )),
                
                # El combo que mencionas: ¿Qué tipo de trámite es?
                ('tipo_nombre', models.CharField(
                    max_length=50, 
                    choices=[
                        ('RECTIFICACION', 'Rectificación'),
                        ('ADECUACION', 'Adecuación'),
                        ('INCORPORACION', 'Incorporación'),
                        ('MODIFICACION', 'Modificación'),
                    ],
                    verbose_name='Tipo de Trámite'
                )),
                
                # El dato que quiere cambiar (El combo que mencionas)
                ('campo_modificado', models.CharField(
                    max_length=50, 
                    verbose_name='Dato a cambiar',
                    help_text="Ej: Color, Peso Bruto, Motor..."
                )),
                
                # La caja con el valor nuevo
                ('valor_nuevo', models.CharField(
                    max_length=255, 
                    verbose_name='Nuevo Valor'
                )),
                
                ('fecha_tramite', models.DateField(auto_now_add=True, verbose_name='Fecha del Trámite')),
            ],
            options={
                'verbose_name': 'Detalle de Trámite',
                'verbose_name_plural': 'Detalles de Trámites',
            },
        ),
    ]