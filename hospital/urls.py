from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
]
