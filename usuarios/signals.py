from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from pacientes.models import Paciente

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
