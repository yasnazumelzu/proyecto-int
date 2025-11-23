from django.urls import path
from . import views

app_name = "usuarioapp"

urlpatterns = [
    path("lista/", views.listar_usuarios, name="lista"),
]