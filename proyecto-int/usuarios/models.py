from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuario(AbstractUser):
    ROLES = [
        ('medico', 'Médico'),
        ('matrona', 'Matrona'),
        ('enfermero', 'Enfermero'),
        ('administrativo', 'Administrativo'),
        ('ti', 'Administrador TI'),
        ('pediatra', 'Pediatra'),
    ]
    rol = models.CharField(max_length=20, choices=ROLES)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"

@receiver(post_save, sender=Usuario)
def asignar_grupo_usuario(sender, instance, created, **kwargs):
    """
    Asigna automáticamente el grupo correcto según el rol al crear un usuario.
    """
    if created and instance.rol:
        grupo, _ = Group.objects.get_or_create(name=instance.get_rol_display())
        instance.groups.add(grupo)
