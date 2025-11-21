"""
Script para crear un usuario Administrador TI
Ejecutar: python manage.py shell < crear_usuario_ti.py
O ejecutar en el shell de Django: python manage.py shell
"""
from usuarios.models import Usuario

# Crear usuario TI
username = 'admin_ti'
email = 'ti@hospital.cl'
password = 'admin123'  # Cambiar por una contraseña segura

# Verificar si el usuario ya existe
if Usuario.objects.filter(username=username).exists():
    print(f"El usuario {username} ya existe.")
    usuario = Usuario.objects.get(username=username)
    usuario.rol = 'ti'
    usuario.is_staff = True
    usuario.is_superuser = True
    usuario.is_active = True
    usuario.save()
    print(f"Usuario {username} actualizado con rol TI.")
else:
    usuario = Usuario.objects.create_user(
        username=username,
        email=email,
        password=password,
        rol='ti',
        is_staff=True,
        is_superuser=True,
        is_active=True
    )
    print(f"Usuario {username} creado exitosamente con rol TI.")
    print(f"Contraseña: {password}")

print("\n" + "="*50)
print("CREDENCIALES DE ACCESO:")
print("="*50)
print(f"Usuario: {username}")
print(f"Contraseña: {password}")
print("="*50)

