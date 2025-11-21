from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Auditoria(models.Model):
    """Modelo para registrar todas las acciones del sistema"""
    ACCION_CHOICES = [
        ('CREATE', 'Crear'),
        ('READ', 'Leer'),
        ('UPDATE', 'Actualizar'),
        ('DELETE', 'Eliminar'),
        ('LOGIN', 'Inicio de Sesión'),
        ('LOGOUT', 'Cierre de Sesión'),
        ('OTHER', 'Otro'),
    ]
    
    METODO_HTTP_CHOICES = [
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('PATCH', 'PATCH'),
        ('DELETE', 'DELETE'),
        ('OPTIONS', 'OPTIONS'),
        ('HEAD', 'HEAD'),
    ]
    
    # Información de la petición
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='acciones_auditoria',
        help_text="Usuario que realizó la acción"
    )
    fecha_hora = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora de la acción")
    metodo_http = models.CharField(max_length=10, choices=METODO_HTTP_CHOICES, help_text="Método HTTP utilizado")
    url = models.CharField(max_length=500, help_text="URL de la petición")
    ruta = models.CharField(max_length=500, blank=True, null=True, help_text="Ruta de la vista")
    nombre_vista = models.CharField(max_length=200, blank=True, null=True, help_text="Nombre de la vista")
    
    # Tipo de acción
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES, help_text="Tipo de acción realizada")
    
    # Información del modelo afectado (si aplica)
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Tipo de modelo afectado"
    )
    object_id = models.PositiveIntegerField(null=True, blank=True, help_text="ID del objeto afectado")
    contenido = GenericForeignKey('content_type', 'object_id')
    nombre_modelo = models.CharField(max_length=200, blank=True, null=True, help_text="Nombre del modelo")
    
    # Datos de la petición
    datos_enviados = models.JSONField(null=True, blank=True, help_text="Datos enviados en la petición")
    datos_respuesta = models.JSONField(null=True, blank=True, help_text="Datos de la respuesta")
    codigo_respuesta = models.IntegerField(null=True, blank=True, help_text="Código HTTP de respuesta")
    
    # Información adicional
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="Dirección IP del cliente")
    user_agent = models.TextField(blank=True, null=True, help_text="User Agent del navegador")
    observaciones = models.TextField(blank=True, null=True, help_text="Observaciones adicionales")
    
    # Estado
    exito = models.BooleanField(default=True, help_text="Indica si la acción fue exitosa")
    mensaje_error = models.TextField(blank=True, null=True, help_text="Mensaje de error si hubo fallo")
    
    class Meta:
        verbose_name = "Registro de Auditoría"
        verbose_name_plural = "Registros de Auditoría"
        ordering = ['-fecha_hora']
        indexes = [
            models.Index(fields=['-fecha_hora']),
            models.Index(fields=['usuario', '-fecha_hora']),
            models.Index(fields=['accion', '-fecha_hora']),
            models.Index(fields=['nombre_modelo', '-fecha_hora']),
        ]
    
    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else "Anónimo"
        return f"{self.get_accion_display()} - {usuario_str} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}"

