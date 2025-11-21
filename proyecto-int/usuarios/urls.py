from django.urls import path
from . import views
from medico import views as medico_views
from matrona import views as matrona_views
from enfermero import views as enfermero_views
from administrativos import views as admin_views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('medico/', medico_views.dashboard_medico, name='dashboard_medico'),
    path('matrona/', matrona_views.dashboard_matrona, name='dashboard_matrona'),
    path('enfermero/', enfermero_views.dashboard_enfermero, name='dashboard_enfermero'),
    path('administrativo/', admin_views.dashboard_admin, name='dashboard_admin'),
]
