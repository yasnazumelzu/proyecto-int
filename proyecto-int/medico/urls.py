from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_medico, name='dashboard_medico'),
    path('revisar-pacientes/', views.revisar_pacientes, name='revisar_pacientes'),
    path('ficha-clinica/<int:id>/', views.ficha_clinica, name='ficha_clinica'),
    path('registrar-reporte/', views.registrar_reporte, name='registrar_reporte'),
    path('reportes/', views.lista_reportes, name='lista_reportes'),
    path('reportes/<int:id>/', views.detalle_reporte, name='detalle_reporte'),
]
