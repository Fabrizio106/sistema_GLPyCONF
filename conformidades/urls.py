from django.urls import path
from . import views

urlpatterns = [
    path('nuevo/', views.crear_certificado_conformidad, name='crear_certificado_conformidad'),
]