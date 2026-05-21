from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.crear_certificado_conformidad, name='crear_certificado_conformidad'),
    path('consultar-historial/', views.consultar_ultima_conformidad, name='consultar_historial'),
]