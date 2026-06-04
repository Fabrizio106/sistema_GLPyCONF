# conformidades/migrations/0001_initial.py
from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CertificadoConformidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                
                # Identificación Básica
                ('numero_vin', models.CharField(max_length=17, unique=True, verbose_name='Número VIN')),
                ('placa', models.CharField(max_length=10, verbose_name='Placa')),
                ('categoria', models.CharField(blank=True, max_length=20, null=True, verbose_name='Categoría')),
                ('marca', models.CharField(blank=True, max_length=50, null=True, verbose_name='Marca')),
                ('modelo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Modelo')),
                ('color', models.CharField(blank=True, max_length=50, null=True, verbose_name='Color')),
                
                # Series y Motor
                ('numero_serie', models.CharField(blank=True, max_length=50, null=True, verbose_name='Número de Serie')),
                ('numero_motor', models.CharField(blank=True, max_length=50, null=True, verbose_name='Número de Motor')),
                ('carroceria', models.CharField(blank=True, max_length=100, null=True, verbose_name='Carrocería')),
                ('potencia', models.CharField(blank=True, max_length=50, null=True, verbose_name='Potencia')),
                ('formula_rodante', models.CharField(blank=True, max_length=20, null=True, verbose_name='Fórmula Rodante')),
                ('combustible', models.CharField(blank=True, max_length=50, null=True, verbose_name='Combustible')),
                
                # Capacidades (Asignados como CharField por si llevan rangos o anotaciones)
                ('asientos', models.CharField(blank=True, max_length=10, null=True, verbose_name='Asientos')),
                ('pasajeros', models.CharField(blank=True, max_length=10, null=True, verbose_name='Pasajeros')),
                ('ruedas', models.CharField(blank=True, max_length=10, null=True, verbose_name='Ruedas')),
                ('ejes', models.CharField(blank=True, max_length=10, null=True, verbose_name='Ejes')),
                ('cilindros', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cilindros')),
                
                # Medidas y Cilindrada
                ('longitud', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Longitud (m)')),
                ('altura', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Altura (m)')),
                ('ancho', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Ancho (m)')),
                ('cilindrada', models.CharField(blank=True, max_length=20, null=True, verbose_name='Cilindrada')),
                
                # Pesos
                ('peso_bruto', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Peso Bruto (kg)')),
                ('peso_neto', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Peso Neto (kg)')),
                ('carga_util', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Carga Útil (kg)')),
                
                # Fabricación y Versión
                ('anio_fabricacion', models.CharField(blank=True, max_length=4, null=True, verbose_name='Año Fab.')),
                ('anio_modelo', models.CharField(blank=True, max_length=4, null=True, verbose_name='Año Modelo')),
                ('version', models.CharField(blank=True, max_length=100, null=True, verbose_name='Versión')),
                
                # Auditoría
                ('fecha_registro', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')),
            ],
            options={
                'verbose_name': 'Certificado de Conformidad',
                'verbose_name_plural': 'Certificados de Conformidad',
            },
        ),
    ]