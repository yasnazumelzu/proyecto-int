from django.db import models

class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=120)
    edad = models.PositiveIntegerField()
    fecha_ingreso = models.DateField(auto_now_add=True)
    diagnostico = models.CharField(max_length=255)
    fecha_nacimiento = models.DateField(null=True, blank=True, help_text="Fecha de nacimiento de la madre")
    comuna = models.CharField(max_length=100, blank=True, null=True)
    cesfam = models.CharField(max_length=100, blank=True, null=True, help_text="Centro de Salud Familiar")
    es_migrante = models.BooleanField(default=False)
    pueblo_originario = models.CharField(max_length=100, blank=True, null=True)
    vih_positivo = models.BooleanField(default=False, help_text="Madre VIH (+)")
    vdrl_resultado = models.CharField(max_length=50, blank=True, null=True, help_text="Resultado examen VDRL")
    vdrl_tratamiento = models.CharField(max_length=255, blank=True, null=True, help_text="Tratamiento VDRL")
    hepatitis_b_resultado = models.CharField(max_length=50, blank=True, null=True, help_text="Resultado examen Hepatitis B")
    hepatitis_b_tratamiento_ig = models.CharField(max_length=255, blank=True, null=True, help_text="Tratamiento con IG")
    hepatitis_b_profilaxis_completa = models.BooleanField(default=False, help_text="Profilaxis Completa (Sí/No)")

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

class RecienNacido(models.Model):
    # Información básica
    paciente_madre = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='recien_nacidos')
    apellido_paterno = models.CharField(max_length=120, blank=True, null=True)
    nombre = models.CharField(max_length=120)
    fecha_nacimiento = models.DateField()
    hora_nacimiento = models.TimeField(blank=True, null=True)
    
    # Datos antropométricos
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en gramos")
    talla = models.DecimalField(max_digits=4, decimal_places=1, help_text="Talla en cm")
    circunferencia_cefalica = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, help_text="CC en cm")
    
    # Tipo de parto y gestación
    TIPO_PARTO_CHOICES = [
        ('normal', 'Normal'),
        ('cesarea', 'Cesárea'),
        ('instrumental', 'Instrumental'),
    ]
    tipo_parto = models.CharField(max_length=20, choices=TIPO_PARTO_CHOICES, blank=True, null=True)
    edad_gestacional_semanas = models.PositiveIntegerField(blank=True, null=True, help_text="Semanas de gestación")
    edad_gestacional_dias = models.PositiveIntegerField(blank=True, null=True, help_text="Días de gestación")
    
    # Sexo
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('I', 'Intersexual'),
    ]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, blank=True, null=True)
    
    # Apgar
    apgar_1min = models.PositiveIntegerField(blank=True, null=True, help_text="APGAR 1 minuto")
    apgar_5min = models.PositiveIntegerField(blank=True, null=True, help_text="APGAR 5 minutos")
    
    # Reanimación
    reanimacion_basica = models.BooleanField(default=False)
    reanimacion_avanzada = models.BooleanField(default=False)
    
    # Gases de cordón
    gases_cordon = models.CharField(max_length=50, blank=True, null=True)
    
    # Apego
    apego = models.CharField(max_length=50, blank=True, null=True)
    apego_canguro = models.BooleanField(default=False)
    apego_tunel = models.BooleanField(default=False)
    lactancia_antes_media_hora = models.BooleanField(default=False, help_text="Lact. antes 1/2 hr")
    lactancia_antes_60min = models.BooleanField(default=False, help_text="Lact. antes 60'")
    
    # Clampado
    clampado_tardio = models.BooleanField(default=False)
    
    # Profilaxis y vacunas
    profilaxis_ocular = models.BooleanField(default=False)
    vacuna_hepatitis_b = models.BooleanField(default=False)
    profesional_vacuna_vhb = models.CharField(max_length=120, blank=True, null=True)
    vacuna_bcg = models.BooleanField(default=False)
    
    # Alojamiento
    alojamiento_conjunto_puerperio = models.BooleanField(default=False, help_text="Alojamiento Conjunto en Puerperio Inmediato")
    acompanante_pabellon = models.BooleanField(default=False, help_text="Acompañante en Pabellón")
    
    # Diagnóstico y malformaciones
    diagnostico = models.TextField(blank=True, null=True)
    malformacion_congenita = models.BooleanField(default=False)
    descripcion_malformacion = models.TextField(blank=True, null=True)
    
    # Destino
    destino_rn = models.CharField(max_length=100, blank=True, null=True, help_text="Destino del recién nacido")
    interno = models.BooleanField(default=False)
    
    # Otros
    int_causal_2 = models.CharField(max_length=100, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno or ''} - hijo/a de {self.paciente_madre.nombre}"
