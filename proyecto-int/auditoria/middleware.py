import json
import logging
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Auditoria

logger = logging.getLogger(__name__)

class AuditoriaMiddleware:
    """
    Middleware para registrar todas las acciones del sistema en la tabla de auditoría.
    Se ejecuta antes de procesar la petición y después de generar la respuesta.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Información antes de procesar la petición
        usuario = getattr(request, 'user', None)
        if usuario and not usuario.is_authenticated:
            usuario = None
        
        # Determinar el tipo de acción basado en el método HTTP
        accion = self._determinar_accion(request.method, request.path)
        
        # Obtener datos de la petición (solo para métodos que envían datos)
        datos_enviados = None
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                # Primero intentar obtener datos del formulario (más común en Django)
                if hasattr(request, 'POST') and request.POST:
                    # Convertir QueryDict a dict normal, limitando el tamaño
                    datos_enviados = {k: v if len(str(v)) < 500 else str(v)[:500] + '...' 
                                     for k, v in request.POST.items()}
                elif hasattr(request, 'body') and request.body:
                    # Intentar parsear JSON
                    try:
                        body_str = request.body.decode('utf-8')
                        if len(body_str) < 10000:  # Limitar tamaño
                            datos_enviados = json.loads(body_str)
                        else:
                            datos_enviados = {'_truncated': True, 'size': len(body_str)}
                    except:
                        pass
            except Exception as e:
                logger.debug(f"Error al obtener datos de la petición: {e}")
                datos_enviados = None
        
        # Obtener información del modelo afectado (si es posible)
        nombre_modelo = None
        object_id = None
        content_type = None
        
        # Intentar determinar el modelo desde la URL o parámetros
        try:
            if hasattr(request, 'resolver_match') and request.resolver_match:
                # Buscar en los parámetros de la URL
                if 'id' in request.resolver_match.kwargs:
                    object_id = request.resolver_match.kwargs.get('id')
                elif 'pk' in request.resolver_match.kwargs:
                    object_id = request.resolver_match.kwargs.get('pk')
                elif 'recien_nacido_id' in request.resolver_match.kwargs:
                    object_id = request.resolver_match.kwargs.get('recien_nacido_id')
                    nombre_modelo = 'reciennacido'
                elif 'admision_id' in request.resolver_match.kwargs:
                    object_id = request.resolver_match.kwargs.get('admision_id')
                    nombre_modelo = 'admision'
                
                # Intentar determinar el modelo desde el nombre de la app en la URL
                path_parts = request.path.strip('/').split('/')
                if len(path_parts) > 0 and not nombre_modelo:
                    app_name = path_parts[0]
                    # Mapeo de apps a modelos comunes
                    modelo_map = {
                        'pacientes': 'paciente',
                        'medico': 'reportemedico',
                        'enfermero': 'controlenfermeria',
                        'administrativo': 'admision',
                        'matrona': 'reciennacido',
                        'pediatra': 'altareciennacido',
                    }
                    if app_name in modelo_map:
                        nombre_modelo = modelo_map[app_name]
        except Exception as e:
            logger.debug(f"No se pudo determinar el modelo: {e}")
        
        # Obtener ContentType si tenemos el nombre del modelo
        if nombre_modelo:
            try:
                # Buscar en todas las apps
                from django.apps import apps
                for app_config in apps.get_app_configs():
                    try:
                        model = apps.get_model(app_config.label, nombre_modelo)
                        content_type = ContentType.objects.get_for_model(model)
                        nombre_modelo = f"{app_config.label}.{nombre_modelo}"
                        break
                    except:
                        continue
            except Exception as e:
                logger.debug(f"No se pudo obtener ContentType: {e}")
        
        # Obtener IP y User Agent
        ip_address = self._get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Obtener nombre de la vista
        nombre_vista = None
        ruta = None
        try:
            if hasattr(request, 'resolver_match') and request.resolver_match:
                nombre_vista = request.resolver_match.view_name
                ruta = request.resolver_match.route
        except:
            pass
        
        # Procesar la petición
        codigo_respuesta = None
        datos_respuesta = None
        exito = True
        mensaje_error = None
        
        try:
            response = self.get_response(request)
            codigo_respuesta = response.status_code
            
            # Determinar si fue exitoso (códigos 2xx y 3xx son exitosos)
            exito = 200 <= codigo_respuesta < 400
            
            # Intentar obtener datos de la respuesta (solo para respuestas JSON)
            if hasattr(response, 'content') and response.get('Content-Type', '').startswith('application/json'):
                try:
                    datos_respuesta = json.loads(response.content.decode('utf-8'))
                except:
                    pass
        except Exception as e:
            exito = False
            mensaje_error = str(e)
            codigo_respuesta = 500
            # Re-lanzar la excepción para que Django la maneje
            raise
        
        # Registrar en la auditoría
        try:
            # No registrar peticiones estáticas ni del admin de Django (opcional)
            if not self._debe_registrar(request.path):
                return response if 'response' in locals() else self.get_response(request)
            
            Auditoria.objects.create(
                usuario=usuario if usuario and usuario.is_authenticated else None,
                metodo_http=request.method,
                url=request.get_full_path(),
                ruta=ruta,
                nombre_vista=nombre_vista,
                accion=accion,
                content_type=content_type,
                object_id=object_id,
                nombre_modelo=nombre_modelo,
                datos_enviados=datos_enviados,
                datos_respuesta=datos_respuesta,
                codigo_respuesta=codigo_respuesta,
                ip_address=ip_address,
                user_agent=user_agent,
                exito=exito,
                mensaje_error=mensaje_error,
            )
        except Exception as e:
            # No fallar la petición si hay error en la auditoría
            logger.error(f"Error al registrar en auditoría: {e}")
        
        return response if 'response' in locals() else self.get_response(request)
    
    def _determinar_accion(self, metodo_http, path):
        """Determina el tipo de acción basado en el método HTTP y la URL"""
        # Login/Logout
        if 'login' in path.lower():
            return 'LOGIN'
        if 'logout' in path.lower():
            return 'LOGOUT'
        
        # CRUD basado en método HTTP
        if metodo_http == 'POST':
            # Verificar si es creación o actualización según la URL
            if any(x in path for x in ['/nuevo/', '/crear/', '/registrar/', '/add/']):
                return 'CREATE'
            elif any(x in path for x in ['/editar/', '/actualizar/', '/update/']):
                return 'UPDATE'
            return 'CREATE'  # Por defecto POST es creación
        elif metodo_http in ['PUT', 'PATCH']:
            return 'UPDATE'
        elif metodo_http == 'DELETE':
            return 'DELETE'
        elif metodo_http == 'GET':
            return 'READ'
        else:
            return 'OTHER'
    
    def _get_client_ip(self, request):
        """Obtiene la dirección IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _debe_registrar(self, path):
        """Determina si debe registrar esta petición"""
        # No registrar peticiones estáticas
        exclusiones = [
            '/static/',
            '/media/',
            '/favicon.ico',
            '/__debug__/',
        ]
        
        for exclusion in exclusiones:
            if exclusion in path:
                return False
        
        return True

