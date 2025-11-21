"""
Script para crear usuario pediatra
Ejecutar: python manage.py shell < crear_pediatra.py
"""
from usuarios.models import Usuario

# Crear usuario pediatra
username = 'pediatra'
email = 'pediatra@hospital.cl'
password = '1234'

# Verificar si el usuario ya existe
if Usuario.objects.filter(username=username).exists():
    print(f"El usuario {username} ya existe.")
    usuario = Usuario.objects.get(username=username)
    usuario.rol = 'pediatra'
    usuario.is_staff = True
    usuario.is_active = True
    usuario.set_password(password)
    usuario.save()
    print(f"Usuario {username} actualizado con rol pediatra.")
else:
    usuario = Usuario.objects.create_user(
        username=username,
        email=email,
        password=password,
        rol='pediatra',
        is_staff=True,
        is_active=True
    )
    print(f"Usuario {username} creado exitosamente con rol pediatra.")

print("\n" + "="*50)
print("CREDENCIALES DE ACCESO:")
print("="*50)
print(f"Usuario: {username}")
print(f"Contraseña: {password}")
print("="*50)

