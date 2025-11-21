from django.db import models
from django.conf import settings
from pacientes.models import RecienNacido

class AltaRecienNacido(models.Model):
    """Modelo para registrar el alta de un recién nacido"""
    TIPO_ALTA_CHOICES = [
        ('alta_normal', 'Alta Normal'),
        ('alta_precoz', 'Alta Precoz'),
        ('traslado', 'Traslado'),
        ('fallecimiento', 'Fallecimiento'),
    ]
    
    CONDICION_ALTA_CHOICES = [
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('grave', 'Grave'),
        ('critica', 'Crítica'),
    ]
    
    recien_nacido = models.OneToOneField(RecienNacido, on_delete=models.CASCADE, related_name='alta')
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_egreso = models.DateTimeField(blank=True, null=True, help_text="Fecha y hora del egreso")
    tipo_alta = models.CharField(max_length=20, choices=TIPO_ALTA_CHOICES, default='alta_normal')
    condicion_alta = models.CharField(max_length=20, choices=CONDICION_ALTA_CHOICES, default='buena')
    
    # Información médica
    diagnostico_final = models.TextField(help_text="Diagnóstico final del recién nacido")
    tratamiento_continuo = models.TextField(blank=True, null=True, help_text="Tratamiento a continuar en casa")
    medicamentos_recetados = models.TextField(blank=True, null=True, help_text="Medicamentos recetados")
    indicaciones_alta = models.TextField(help_text="Indicaciones para el alta")
    controles_programados = models.TextField(blank=True, null=True, help_text="Controles programados")
    
    # Vacunación
    vacunas_aplicadas = models.TextField(blank=True, null=True, help_text="Vacunas aplicadas durante la estadía")
    vacunas_pendientes = models.TextField(blank=True, null=True, help_text="Vacunas pendientes")
    
    # Alimentación
    tipo_alimentacion = models.CharField(max_length=100, blank=True, null=True, help_text="Tipo de alimentación al alta")
    peso_alta = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Peso al alta (gramos)")
    
    # Seguimiento
    requiere_seguimiento = models.BooleanField(default=False)
    motivo_seguimiento = models.TextField(blank=True, null=True)
    fecha_control_proximo = models.DateField(blank=True, null=True)
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    pediatra_responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='altas_recien_nacidos')
    
    class Meta:
        verbose_name = "Alta de Recién Nacido"
        verbose_name_plural = "Altas de Recién Nacidos"
        ordering = ['-fecha_alta']
    
    def __str__(self):
        return f"Alta RN {self.id} - {self.recien_nacido.nombre} - {self.fecha_alta.strftime('%d/%m/%Y')}"

