from django.contrib import admin
from .models import Auditoria

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'usuario', 'accion', 'metodo_http', 'nombre_modelo', 'url', 'exito', 'codigo_respuesta')
    list_filter = ('accion', 'metodo_http', 'exito', 'fecha_hora', 'nombre_modelo')
    search_fields = ('usuario__username', 'url', 'nombre_vista', 'nombre_modelo', 'ip_address')
    readonly_fields = ('fecha_hora', 'usuario', 'metodo_http', 'url', 'ruta', 'nombre_vista', 
                      'accion', 'content_type', 'object_id', 'nombre_modelo', 'datos_enviados', 
                      'datos_respuesta', 'codigo_respuesta', 'ip_address', 'user_agent', 
                      'exito', 'mensaje_error')
    date_hierarchy = 'fecha_hora'
    ordering = ('-fecha_hora',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('fecha_hora', 'usuario', 'metodo_http', 'url', 'ruta', 'nombre_vista', 'accion')
        }),
        ('Modelo Afectado', {
            'fields': ('content_type', 'object_id', 'nombre_modelo')
        }),
        ('Datos', {
            'fields': ('datos_enviados', 'datos_respuesta')
        }),
        ('Información Técnica', {
            'fields': ('codigo_respuesta', 'ip_address', 'user_agent', 'exito', 'mensaje_error', 'observaciones')
        }),
    )
    
    def has_add_permission(self, request):
        return False  # No permitir crear registros manualmente
    
    def has_change_permission(self, request, obj=None):
        return False  # No permitir editar registros
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Solo superusuarios pueden eliminar

