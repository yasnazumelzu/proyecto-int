from django.contrib import admin
from django.urls import path, include
from usuarios import views as usuario_views
from medico import views as medico_views
from matrona import views as matrona_views
from enfermero import views as enfermero_views
from administrativos import views as admin_views
from homeApp import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', usuario_views.inicio, name='inicio'),
    path('login/', usuario_views.login_view, name='login'),  
    path('logout/', usuario_views.logout_view, name='logout'),
    path('medico/', include('medico.urls')),
    path('matrona/', include('matrona.urls')),
    path('enfermero/', include('enfermero.urls')),
    path('administrativo/', include('administrativos.urls')),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('ti/', include('usuarios.ti_urls')),
    path('pacientes/', include('pacientes.urls')),
    path('pediatra/', include('pediatra.urls')),
    path('auditoria/', include('auditoria.urls')),
    path("usuarios/", include("UsuarioApp.urls")),
    path("", include("homeApp.urls")),
]
