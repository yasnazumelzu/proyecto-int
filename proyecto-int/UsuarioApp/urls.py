from django.urls import path
from . import views

app_name = "usuarios_app"

urlpatterns = [
    path("lista/", views.listar_usuarios, name="lista"),
]