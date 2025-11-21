from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'

    def ready(self):
        # Ejecutar solo cuando las apps ya estén cargadas
        from django.db.models.signals import post_migrate
        from .signals import crear_grupos_permisos
        post_migrate.connect(crear_grupos_permisos, sender=self)
