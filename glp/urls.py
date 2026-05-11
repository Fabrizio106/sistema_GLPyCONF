from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.registrar_certificado_glp, name='registrar_glp'),
    path('historial/', views.historial_glp, name='historial_glp'),
    path('descargar-pdf/<int:pk>/', views.descargar_pdf_glp, name='descargar_pdf_glp'),
    path('configuracion-sedes/', views.gestion_sedes, name='gestion_sedes'),
    path('configuracion-sedes/editar/<int:pk>/', views.gestion_sedes, name='editar_sede'),
    path('configuracion-sedes/eliminar/<int:pk>/', views.eliminar_sede, name='eliminar_sede'),
    path('editar/<int:pk>/', views.editar_certificado_glp, name='editar_glp'),
    path('eliminar/<int:pk>/', views.eliminar_certificado_glp, name='eliminar_glp'),
    path('reportes/', views.reporte_glp_admin, name='reporte_glp_admin'),

]