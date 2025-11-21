from django import forms
from .models import ReporteMedico
from pacientes.models import Paciente

class ReporteMedicoForm(forms.ModelForm):
    class Meta:
        model = ReporteMedico
        fields = [
            'paciente',
            'fecha_consulta',
            'motivo_consulta',
            'sintomas',
            'diagnostico',
            'tratamiento',
            'observaciones',
            'examenes_solicitados',
            'medicamentos_recetados',
            'estado',
            'requiere_seguimiento',
            'fecha_proxima_consulta',
        ]
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_consulta': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo_consulta': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'sintomas': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tratamiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'examenes_solicitados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medicamentos_recetados': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'requiere_seguimiento': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_proxima_consulta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.all().order_by('nombre')

