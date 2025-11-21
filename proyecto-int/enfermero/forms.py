from django import forms
from .models import ControlEnfermeria
from pacientes.models import Paciente

class ControlEnfermeriaForm(forms.ModelForm):
    class Meta:
        model = ControlEnfermeria
        fields = [
            'paciente',
            'presion_arterial_sistolica',
            'presion_arterial_diastolica',
            'frecuencia_cardiaca',
            'frecuencia_respiratoria',
            'temperatura',
            'saturacion_oxigeno',
            'peso',
            'observaciones',
            'medicamentos_administrados',
            'alertas',
            'motivo_alerta',
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'presion_arterial_sistolica': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mmHg'}),
            'presion_arterial_diastolica': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'mmHg'}),
            'frecuencia_cardiaca': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'lpm'}),
            'frecuencia_respiratoria': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'rpm'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '°C'}),
            'saturacion_oxigeno': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '%'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'kg'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'medicamentos_administrados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alertas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'motivo_alerta': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all().order_by('nombre')

