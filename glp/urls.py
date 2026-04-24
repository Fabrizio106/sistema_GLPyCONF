from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.crear_certificado_glp, name='crear_glp'),
    path('historial/', views.historial_glp, name='historial_glp'),
    path('descargar-pdf/<int:pk>/', views.descargar_pdf_glp, name='descargar_pdf_glp'),
]