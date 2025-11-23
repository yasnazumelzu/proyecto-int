from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from PIL import Image

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

class Perfil(models.Model):
    ROLES_BASE = [
        ('ADMIN', 'Administrador'),
        ('GERENCIA', 'Gerencia'),
        ('NORMAL', 'Usuario Normal'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Rol administrativo del sistema modular
    rol_base = models.CharField(max_length=20, choices=ROLES_BASE, default='NORMAL')

    # Foto de perfil
    foto = models.ImageField(upload_to="perfiles/", null=True, blank=True)

    # Último acceso
    ultimo_acceso = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Reducción y recorte
        if self.foto:
            from utils.images import procesar_foto
            procesar_foto(self.foto.path)
