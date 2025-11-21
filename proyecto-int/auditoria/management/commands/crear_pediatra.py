from django.core.management.base import BaseCommand
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Crea o actualiza el usuario pediatra con contraseña 1234'

    def handle(self, *args, **options):
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
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario {username} actualizado exitosamente.')
            )
        except Usuario.DoesNotExist:
            usuario = Usuario.objects.create_user(
                username=username,
                email=email,
                password=password,
                rol='pediatra',
                is_staff=True,
                is_active=True
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario {username} creado exitosamente.')
            )

        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('CREDENCIALES DE ACCESO:'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(self.style.SUCCESS(f'Usuario: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Contraseña: {password}'))
        self.stdout.write(self.style.SUCCESS('='*50))

