from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuario_views
from medico import views as medico_views
from matrona import views as matrona_views
from enfermero import views as enfermero_views
from administrativos import views as admin_views

urlpatterns = [
    path('', usuario_views.inicio, name='inicio'),
    path('login/', usuario_views.login_view, name='login'),  
    path('logout/', usuario_views.logout_view, name='logout'),
    path('medico/', medico_views.dashboard_medico, name='dashboard_medico'),
    path('matrona/', matrona_views.dashboard_matrona, name='dashboard_matrona'),
    path('enfermero/', enfermero_views.dashboard_enfermero, name='dashboard_enfermero'),
    path('administrativo/', admin_views.dashboard_admin, name='dashboard_admin'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
]
