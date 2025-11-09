from django import forms
from .models import Paciente, RecienNacido

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['rut', 'nombre', 'edad', 'diagnostico']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'diagnostico': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RecienNacidoForm(forms.ModelForm):
    class Meta:
        model = RecienNacido
        fields = ['nombre', 'peso', 'talla', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'talla': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }
