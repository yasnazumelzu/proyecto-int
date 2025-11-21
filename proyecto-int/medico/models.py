from django.db import models
from django.conf import settings
from pacientes.models import Paciente

class ReporteMedico(models.Model):
    """Modelo para reportes médicos"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('urgente', 'Urgente'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='reportes_medicos')
    fecha_reporte = models.DateTimeField(auto_now_add=True)
    fecha_consulta = models.DateTimeField(blank=True, null=True)
    
    # Información médica
    motivo_consulta = models.TextField(help_text="Motivo de la consulta")
    sintomas = models.TextField(blank=True, null=True)
    diagnostico = models.TextField(help_text="Diagnóstico médico")
    tratamiento = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    examenes_solicitados = models.TextField(blank=True, null=True, help_text="Exámenes solicitados")
    medicamentos_recetados = models.TextField(blank=True, null=True)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    requiere_seguimiento = models.BooleanField(default=False)
    fecha_proxima_consulta = models.DateField(blank=True, null=True)
    
    # Usuario que registra
    medico_responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reportes_registrados')
    
    class Meta:
        ordering = ['-fecha_reporte']
        verbose_name = 'Reporte Médico'
        verbose_name_plural = 'Reportes Médicos'
    
    def __str__(self):
        return f"Reporte {self.id} - {self.paciente.nombre} - {self.fecha_reporte.strftime('%d/%m/%Y')}"
