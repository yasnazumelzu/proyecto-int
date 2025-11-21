from django.contrib import admin
from .models import AltaRecienNacido

@admin.register(AltaRecienNacido)
class AltaRecienNacidoAdmin(admin.ModelAdmin):
    list_display = ('recien_nacido', 'fecha_alta', 'tipo_alta', 'condicion_alta', 'pediatra_responsable')
    list_filter = ('tipo_alta', 'condicion_alta', 'fecha_alta')
    search_fields = ('recien_nacido__nombre', 'recien_nacido__apellido_paterno', 'recien_nacido__paciente_madre__nombre')

