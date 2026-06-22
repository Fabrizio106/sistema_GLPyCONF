from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.crear_certificado_conformidad, name='crear_certificado_conformidad'),
    path('historial/', views.historial_conformidades, name='historial_conformidades'),
    path('eliminar/<int:pk>/', views.eliminar_conformidad, name='eliminar_conformidad'),
    path('pdf/<int:pk>/',      views.descargar_pdf_conformidad,      name='pdf_conformidad'),
    path('editar/<int:pk>/', views.editar_conformidad, name='editar_conformidad'),
    path('consultar-historial/', views.consultar_ultima_conformidad, name='consultar_historial'),
    path('sedes/', views.gestion_sedes_conformidad, name='gestion_sedes_conformidad'),
    path('sedes/editar/<int:pk>/', views.editar_sede_conformidad, name='editar_sede_conformidad'),
    path('sedes/eliminar/<int:pk>/', views.eliminar_sede_conformidad, name='eliminar_sede_conformidad'),
    path('reporte-admin/', views.reporte_cmd_admin, name='reporte_cmd_admin'),
    path('reporte-admin/excel/', views.descargar_excel_cmd, name='descargar_excel_cmd'),
]