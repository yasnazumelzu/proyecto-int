from django import forms
from .models import AltaRecienNacido
from pacientes.models import RecienNacido

class AltaRecienNacidoForm(forms.ModelForm):
    class Meta:
        model = AltaRecienNacido
        fields = [
            'recien_nacido',
            'fecha_egreso',
            'tipo_alta',
            'condicion_alta',
            'diagnostico_final',
            'tratamiento_continuo',
            'medicamentos_recetados',
            'indicaciones_alta',
            'controles_programados',
            'vacunas_aplicadas',
            'vacunas_pendientes',
            'tipo_alimentacion',
            'peso_alta',
            'requiere_seguimiento',
            'motivo_seguimiento',
            'fecha_control_proximo',
            'observaciones',
        ]
        widgets = {
            'recien_nacido': forms.Select(attrs={'class': 'form-control'}),
            'fecha_egreso': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'tipo_alta': forms.Select(attrs={'class': 'form-control'}),
            'condicion_alta': forms.Select(attrs={'class': 'form-control'}),
            'diagnostico_final': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'tratamiento_continuo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medicamentos_recetados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'indicaciones_alta': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'controles_programados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vacunas_aplicadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'vacunas_pendientes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tipo_alimentacion': forms.TextInput(attrs={'class': 'form-control'}),
            'peso_alta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'requiere_seguimiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'motivo_seguimiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_control_proximo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo recién nacidos que no tengan alta registrada
        self.fields['recien_nacido'].queryset = RecienNacido.objects.filter(
            alta__isnull=True
        ).order_by('-fecha_nacimiento')

