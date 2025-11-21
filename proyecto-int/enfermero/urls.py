from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_enfermero, name='dashboard_enfermero'),
    path('registrar-control/', views.registrar_control, name='registrar_control'),
    path('controles/', views.lista_controles, name='lista_controles'),
    path('consultar-pacientes/', views.consultar_pacientes, name='consultar_pacientes'),
    path('paciente/<int:id>/', views.detalle_paciente_enfermero, name='detalle_paciente_enfermero'),
]
