from django.db import models

class Paciente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=120)
    edad = models.PositiveIntegerField()
    fecha_ingreso = models.DateField(auto_now_add=True)
    diagnostico = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"

class RecienNacido(models.Model):
    paciente_madre = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='recien_nacidos')
    nombre = models.CharField(max_length=120)
    peso = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en Kg")
    talla = models.DecimalField(max_digits=4, decimal_places=1, help_text="Talla en cm")
    fecha_nacimiento = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} - hijo/a de {self.paciente_madre.nombre}"
