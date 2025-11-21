import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital.settings')
django.setup()

from usuarios.models import Usuario

username = 'pediatra'
email = 'pediatra@hospital.cl'
password = '1234'

try:
    usuario = Usuario.objects.get(username=username)
    usuario.rol = 'pediatra'
    usuario.is_staff = True
    usuario.is_active = True
    usuario.set_password(password)
    usuario.save()
    print(f"Usuario {username} actualizado. Contraseña: {password}")
except Usuario.DoesNotExist:
    usuario = Usuario.objects.create_user(
        username=username,
        email=email,
        password=password,
        rol='pediatra',
        is_staff=True,
        is_active=True
    )
    print(f"Usuario {username} creado. Contraseña: {password}")

print(f"\nUsuario: {username}")
print(f"Contraseña: {password}")

