from django.db import models
from pacientes.models import Paciente
from django.conf import settings

class Admision(models.Model):
    """Modelo para registrar las admisiones de pacientes al hospital"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    
    TIPO_ADMISION_CHOICES = [
        ('urgencia', 'Urgencia'),
        ('programada', 'Programada'),
        ('parto', 'Parto'),
        ('consulta', 'Consulta'),
    ]
    
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='admissions')
    fecha_admision = models.DateTimeField(auto_now_add=True)
    tipo_admision = models.CharField(max_length=20, choices=TIPO_ADMISION_CHOICES, default='consulta')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    motivo_admision = models.TextField(help_text="Motivo de la admisión")
    servicio = models.CharField(max_length=100, blank=True, null=True, help_text="Servicio o área de atención")
    medico_responsable = models.CharField(max_length=120, blank=True, null=True)
    numero_habitacion = models.CharField(max_length=20, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_alta = models.DateTimeField(blank=True, null=True)
    usuario_registro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='admissions_registered')
    
    class Meta:
        verbose_name = "Admisión"
        verbose_name_plural = "Admisiones"
        ordering = ['-fecha_admision']
    
    def __str__(self):
        return f"Admisión {self.id} - {self.paciente.nombre} ({self.get_estado_display()})"

class Pago(models.Model):
    """Modelo para registrar los pagos realizados por pacientes"""
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('parcial', 'Pago Parcial'),
        ('cancelado', 'Cancelado'),
        ('reembolsado', 'Reembolsado'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('transferencia', 'Transferencia Bancaria'),
        ('cheque', 'Cheque'),
        ('fonasa', 'FONASA'),
        ('isapre', 'ISAPRE'),
        ('particular', 'Particular'),
    ]
    
    admision = models.ForeignKey(Admision, on_delete=models.CASCADE, related_name='pagos', null=True, blank=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='pagos')
    fecha_pago = models.DateTimeField(auto_now_add=True)
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto total a pagar")
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Monto pagado hasta ahora")
    monto_pendiente = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto pendiente")
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    concepto = models.CharField(max_length=255, help_text="Concepto del pago (consulta, procedimiento, etc.)")
    numero_comprobante = models.CharField(max_length=50, blank=True, null=True, help_text="Número de comprobante o boleta")
    numero_transaccion = models.CharField(max_length=50, blank=True, null=True, help_text="Número de transacción bancaria")
    observaciones = models.TextField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True, help_text="Fecha de vencimiento del pago")
    usuario_registro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='pagos_registered')
    
    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha_pago']
    
    def __str__(self):
        return f"Pago {self.id} - {self.paciente.nombre} - ${self.monto_total}"
    
    def save(self, *args, **kwargs):
        # Calcular monto pendiente automáticamente
        self.monto_pendiente = self.monto_total - self.monto_pagado
        # Actualizar estado según el monto pagado
        if self.monto_pendiente <= 0:
            self.estado = 'pagado'
        elif self.monto_pagado > 0:
            self.estado = 'parcial'
        super().save(*args, **kwargs)

class AltaEgreso(models.Model):
    """Modelo para gestionar altas y egresos de pacientes"""
    ESTADO_EPISODIO_CHOICES = [
        ('abierto', 'Abierto'),
        ('cerrado', 'Cerrado'),
    ]
    
    TIPO_ALTA_CHOICES = [
        ('alta_medica', 'Alta Médica'),
        ('alta_voluntaria', 'Alta Voluntaria'),
        ('traslado', 'Traslado'),
        ('fallecimiento', 'Fallecimiento'),
        ('alta_administrativa', 'Alta Administrativa'),
    ]
    
    admision = models.OneToOneField(Admision, on_delete=models.CASCADE, related_name='alta_egreso')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='altas_egresos')
    fecha_alta = models.DateTimeField(auto_now_add=True)
    tipo_alta = models.CharField(max_length=20, choices=TIPO_ALTA_CHOICES, default='alta_medica')
    estado_episodio = models.CharField(max_length=20, choices=ESTADO_EPISODIO_CHOICES, default='abierto')
    
    # Documentos entregados
    documento_alta_entregado = models.BooleanField(default=False, help_text="Documento de alta entregado a la familia")
    certificado_defuncion_entregado = models.BooleanField(default=False, help_text="Certificado de defunción entregado (si aplica)")
    informe_medico_entregado = models.BooleanField(default=False, help_text="Informe médico entregado")
    recetas_entregadas = models.BooleanField(default=False, help_text="Recetas médicas entregadas")
    otros_documentos = models.TextField(blank=True, null=True, help_text="Otros documentos entregados")
    fecha_entrega_documentos = models.DateTimeField(blank=True, null=True)
    persona_que_recibio = models.CharField(max_length=200, blank=True, null=True, help_text="Nombre de la persona que recibió los documentos")
    
    # Trámites administrativos
    pagos_completados = models.BooleanField(default=False, help_text="Pagos completados")
    facturacion_cerrada = models.BooleanField(default=False, help_text="Facturación cerrada")
    habitacion_liberada = models.BooleanField(default=False, help_text="Habitación liberada")
    expediente_clinico_archivado = models.BooleanField(default=False, help_text="Expediente clínico archivado")
    notificaciones_enviadas = models.BooleanField(default=False, help_text="Notificaciones enviadas")
    tramites_adicionales = models.TextField(blank=True, null=True, help_text="Trámites administrativos adicionales realizados")
    
    # Observaciones
    observaciones = models.TextField(blank=True, null=True)
    usuario_registro = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='altas_registradas')
    
    class Meta:
        verbose_name = "Alta y Egreso"
        verbose_name_plural = "Altas y Egresos"
        ordering = ['-fecha_alta']
    
    def __str__(self):
        return f"Alta {self.id} - {self.paciente.nombre} - {self.fecha_alta.strftime('%d/%m/%Y')}"
