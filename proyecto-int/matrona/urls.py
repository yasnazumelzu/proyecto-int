from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_matrona, name='dashboard_matrona'),
    path('registrar-nacimiento/', views.registrar_nacimiento, name='registrar_nacimiento'),
    path('seguimiento-materno/', views.seguimiento_materno, name='seguimiento_materno'),
]
