from django.db import models
from django.contrib.auth.models import User
from utils.images import procesar_foto_perfil
from django.conf import settings

class Perfil(models.Model):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('GERENCIA', 'Gerencia'),
        ('NORMAL', 'Usuario normal'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='NORMAL')
    foto = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    ultimo_acceso = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        procesar_foto_perfil(self)

