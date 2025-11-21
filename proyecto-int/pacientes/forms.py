from django import forms
from .models import Paciente, RecienNacido

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['rut', 'nombre', 'edad', 'diagnostico', 'fecha_nacimiento', 'comuna', 'cesfam', 
                  'es_migrante', 'pueblo_originario', 'vih_positivo', 'vdrl_resultado', 
                  'vdrl_tratamiento', 'hepatitis_b_resultado', 'hepatitis_b_tratamiento_ig', 
                  'hepatitis_b_profilaxis_completa']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'diagnostico': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
            'cesfam': forms.TextInput(attrs={'class': 'form-control'}),
            'es_migrante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pueblo_originario': forms.TextInput(attrs={'class': 'form-control'}),
            'vih_positivo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vdrl_resultado': forms.TextInput(attrs={'class': 'form-control'}),
            'vdrl_tratamiento': forms.TextInput(attrs={'class': 'form-control'}),
            'hepatitis_b_resultado': forms.TextInput(attrs={'class': 'form-control'}),
            'hepatitis_b_tratamiento_ig': forms.TextInput(attrs={'class': 'form-control'}),
            'hepatitis_b_profilaxis_completa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RecienNacidoForm(forms.ModelForm):
    class Meta:
        model = RecienNacido
        fields = [
            # Información básica
            'apellido_paterno', 'nombre', 'fecha_nacimiento', 'hora_nacimiento',
            # Datos antropométricos
            'peso', 'talla', 'circunferencia_cefalica',
            # Tipo de parto y gestación
            'tipo_parto', 'edad_gestacional_semanas', 'edad_gestacional_dias',
            # Sexo
            'sexo',
            # Apgar
            'apgar_1min', 'apgar_5min',
            # Reanimación
            'reanimacion_basica', 'reanimacion_avanzada',
            # Gases de cordón
            'gases_cordon',
            # Apego
            'apego', 'apego_canguro', 'apego_tunel', 'lactancia_antes_media_hora', 'lactancia_antes_60min',
            # Clampado
            'clampado_tardio',
            # Profilaxis y vacunas
            'profilaxis_ocular', 'vacuna_hepatitis_b', 'profesional_vacuna_vhb', 'vacuna_bcg',
            # Alojamiento
            'alojamiento_conjunto_puerperio', 'acompanante_pabellon',
            # Diagnóstico y malformaciones
            'diagnostico', 'malformacion_congenita', 'descripcion_malformacion',
            # Destino
            'destino_rn', 'interno',
            # Otros
            'int_causal_2', 'observaciones',
        ]
        widgets = {
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_nacimiento': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'talla': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'circunferencia_cefalica': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'tipo_parto': forms.Select(attrs={'class': 'form-control'}),
            'edad_gestacional_semanas': forms.NumberInput(attrs={'class': 'form-control'}),
            'edad_gestacional_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'apgar_1min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'apgar_5min': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '10'}),
            'reanimacion_basica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reanimacion_avanzada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'gases_cordon': forms.TextInput(attrs={'class': 'form-control'}),
            'apego': forms.TextInput(attrs={'class': 'form-control'}),
            'apego_canguro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'apego_tunel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lactancia_antes_media_hora': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lactancia_antes_60min': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'clampado_tardio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profilaxis_ocular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vacuna_hepatitis_b': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profesional_vacuna_vhb': forms.TextInput(attrs={'class': 'form-control'}),
            'vacuna_bcg': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alojamiento_conjunto_puerperio': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'acompanante_pabellon': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'malformacion_congenita': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descripcion_malformacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'destino_rn': forms.TextInput(attrs={'class': 'form-control'}),
            'interno': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'int_causal_2': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
