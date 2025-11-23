from django.contrib import admin
from django.urls import path, include
from homeApp import views as home_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', home_views.dashboard, name='inicio'),
    path('login/', usuario_views.login_view, name='login'),  
    path('logout/', usuario_views.logout_view, name='logout'),
    path('medico/', include('medico.urls')),
    path('matrona/', include('matrona.urls')),
    path('enfermero/', include('enfermero.urls')),
    path('administrativo/', include('administrativos.urls')),
    path('pacientes/', include('pacientes.urls')),
    path('pediatra/', include('pediatra.urls')),
    path('auditoria/', include('auditoria.urls')),
    path("usuarios/", include("UsuarioApp.urls")),
    path("accounts/", include("allauth.urls")),
    path("gestion-usuarios/", include("UsuarioApp.urls")),
    path("", include("homeApp.urls")),
]
