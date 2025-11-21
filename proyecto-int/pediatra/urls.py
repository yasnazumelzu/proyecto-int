from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_pediatra, name='dashboard_pediatra'),
    path('recien-nacidos/', views.lista_recien_nacidos, name='lista_recien_nacidos'),
    path('recien-nacidos/<int:id>/', views.detalle_recien_nacido, name='detalle_recien_nacido'),
    path('altas/registrar/', views.registrar_alta_recien_nacido, name='registrar_alta_recien_nacido'),
    path('altas/registrar/<int:recien_nacido_id>/', views.registrar_alta_recien_nacido, name='registrar_alta_recien_nacido_id'),
    path('altas/', views.lista_altas_recien_nacidos, name='lista_altas_recien_nacidos'),
]

