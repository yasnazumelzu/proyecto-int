from django.db import models
from django.conf import settings
from pacientes.models import Paciente

class ControlEnfermeria(models.Model):
    """Modelo para registrar controles de enfermería"""
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='controles_enfermeria')
    fecha_control = models.DateTimeField(auto_now_add=True)
    
    # Signos vitales
    presion_arterial_sistolica = models.IntegerField(blank=True, null=True, help_text="mmHg")
    presion_arterial_diastolica = models.IntegerField(blank=True, null=True, help_text="mmHg")
    frecuencia_cardiaca = models.IntegerField(blank=True, null=True, help_text="lpm")
    frecuencia_respiratoria = models.IntegerField(blank=True, null=True, help_text="rpm")
    temperatura = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="°C")
    saturacion_oxigeno = models.IntegerField(blank=True, null=True, help_text="%")
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="kg")
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    medicamentos_administrados = models.TextField(blank=True, null=True, help_text="Lista de medicamentos administrados")
    alertas = models.BooleanField(default=False, help_text="Requiere atención especial")
    motivo_alerta = models.TextField(blank=True, null=True)
    
    # Usuario que registra
    usuario_registro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='controles_registrados')
    
    class Meta:
        ordering = ['-fecha_control']
        verbose_name = 'Control de Enfermería'
        verbose_name_plural = 'Controles de Enfermería'
    
    def __str__(self):
        return f"Control {self.id} - {self.paciente.nombre} - {self.fecha_control.strftime('%d/%m/%Y %H:%M')}"
