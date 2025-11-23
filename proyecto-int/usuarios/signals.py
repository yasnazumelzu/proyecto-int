from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from pacientes.models import Paciente
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Perfil

def crear_grupos_permisos(sender, **kwargs):
    content_type = ContentType.objects.get_for_model(Paciente)

    grupos_permisos = {
        'Médico': ['view_paciente', 'change_paciente'],
        'Matrona': ['view_paciente', 'add_paciente'],
        'Enfermero': ['view_paciente'],
        'Administrativo': ['add_user', 'change_user', 'delete_user'],
    }

    for nombre, perms in grupos_permisos.items():
        grupo, _ = Group.objects.get_or_create(name=nombre)
        for codename in perms:
            try:
                permiso = Permission.objects.get(codename=codename)
                grupo.permissions.add(permiso)
            except Permission.DoesNotExist:
                continue

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def crear_perfil(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)
