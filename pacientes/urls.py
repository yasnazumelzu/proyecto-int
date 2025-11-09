from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_pacientes, name='lista_pacientes'),
    path('nuevo/', views.nuevo_paciente, name='nuevo_paciente'),
    path('<int:id>/', views.detalle_paciente, name='detalle_paciente'),
    path('<int:paciente_id>/nuevo_recien/', views.nuevo_recien_nacido, name='nuevo_recien_nacido'),
]
