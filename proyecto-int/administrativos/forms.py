from django import forms
from .models import Admision, Pago, AltaEgreso
from pacientes.models import Paciente

class AdmisionForm(forms.ModelForm):
    class Meta:
        model = Admision
        fields = [
            'paciente', 'tipo_admision', 'estado', 'motivo_admision',
            'servicio', 'medico_responsable', 'numero_habitacion', 'observaciones'
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'tipo_admision': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'motivo_admision': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'servicio': forms.TextInput(attrs={'class': 'form-control'}),
            'medico_responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_habitacion': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = [
            'admision', 'paciente', 'monto_total', 'monto_pagado',
            'metodo_pago', 'estado', 'concepto', 'numero_comprobante',
            'numero_transaccion', 'observaciones', 'fecha_vencimiento'
        ]
        widgets = {
            'admision': forms.Select(attrs={'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monto_pagado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'concepto': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_comprobante': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_transaccion': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AltaEgresoForm(forms.ModelForm):
    class Meta:
        model = AltaEgreso
        fields = [
            'admision', 'paciente', 'tipo_alta', 'estado_episodio',
            'documento_alta_entregado', 'certificado_defuncion_entregado',
            'informe_medico_entregado', 'recetas_entregadas', 'otros_documentos',
            'fecha_entrega_documentos', 'persona_que_recibio',
            'pagos_completados', 'facturacion_cerrada', 'habitacion_liberada',
            'expediente_clinico_archivado', 'notificaciones_enviadas',
            'tramites_adicionales', 'observaciones'
        ]
        widgets = {
            'admision': forms.Select(attrs={'class': 'form-control'}),
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'tipo_alta': forms.Select(attrs={'class': 'form-control'}),
            'estado_episodio': forms.Select(attrs={'class': 'form-control'}),
            'documento_alta_entregado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'certificado_defuncion_entregado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'informe_medico_entregado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recetas_entregadas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'otros_documentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_entrega_documentos': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'persona_que_recibio': forms.TextInput(attrs={'class': 'form-control'}),
            'pagos_completados': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'facturacion_cerrada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'habitacion_liberada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'expediente_clinico_archivado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notificaciones_enviadas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tramites_adicionales': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

