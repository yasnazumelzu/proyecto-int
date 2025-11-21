from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('admisiones/', views.lista_admisiones, name='lista_admisiones'),
    path('admisiones/nueva/', views.nueva_admision, name='nueva_admision'),
    path('admisiones/<int:id>/', views.detalle_admision, name='detalle_admision'),
    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/nuevo/', views.nuevo_pago, name='nuevo_pago'),
    path('pagos/nuevo/<int:admision_id>/', views.nuevo_pago, name='nuevo_pago_admision'),
    path('reportes/', views.reportes_generales, name='reportes_generales'),
    path('reportes/exportar-pdf/', views.exportar_reporte_pdf, name='exportar_reporte_pdf'),
    path('reportes/exportar-excel/', views.exportar_reporte_excel, name='exportar_reporte_excel'),
    path('altas-egresos/', views.lista_altas_egresos, name='lista_altas_egresos'),
    path('altas-egresos/registrar/', views.registrar_alta, name='registrar_alta'),
    path('altas-egresos/registrar/<int:admision_id>/', views.registrar_alta, name='registrar_alta_admision'),
    path('altas-egresos/<int:id>/', views.detalle_alta_egreso, name='detalle_alta_egreso'),
    path('altas-egresos/<int:id>/cerrar-episodio/', views.cerrar_episodio, name='cerrar_episodio'),
    path('altas-egresos/<int:id>/entregar-documentos/', views.entregar_documentos, name='entregar_documentos'),
    path('altas-egresos/<int:id>/tramites/', views.tramites_administrativos, name='tramites_administrativos'),
]
