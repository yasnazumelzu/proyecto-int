from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Q
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Auditoria

def es_admin_ti_o_superuser(user):
    """Verifica si el usuario es administrador TI o superusuario"""
    return user.is_authenticated and (user.is_superuser or (hasattr(user, 'rol') and user.rol == 'ti'))

@login_required
@user_passes_test(es_admin_ti_o_superuser, login_url='login')
def lista_auditoria(request):
    """Lista todos los registros de auditoría"""
    registros = Auditoria.objects.all().select_related('usuario', 'content_type').order_by('-fecha_hora')
    
    # Filtros
    usuario_filter = request.GET.get('usuario', '')
    accion_filter = request.GET.get('accion', '')
    metodo_filter = request.GET.get('metodo', '')
    modelo_filter = request.GET.get('modelo', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    solo_exitosos = request.GET.get('solo_exitosos', '')
    
    if usuario_filter:
        registros = registros.filter(usuario__username__icontains=usuario_filter)
    if accion_filter:
        registros = registros.filter(accion=accion_filter)
    if metodo_filter:
        registros = registros.filter(metodo_http=metodo_filter)
    if modelo_filter:
        registros = registros.filter(nombre_modelo__icontains=modelo_filter)
    if fecha_desde:
        registros = registros.filter(fecha_hora__date__gte=fecha_desde)
    if fecha_hasta:
        registros = registros.filter(fecha_hora__date__lte=fecha_hasta)
    if solo_exitosos:
        registros = registros.filter(exito=True)
    
    # Paginación
    paginator = Paginator(registros, 50)  # 50 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Estadísticas
    total_registros = registros.count()
    total_creaciones = registros.filter(accion='CREATE').count()
    total_lecturas = registros.filter(accion='READ').count()
    total_actualizaciones = registros.filter(accion='UPDATE').count()
    total_eliminaciones = registros.filter(accion='DELETE').count()
    total_errores = registros.filter(exito=False).count()
    
    context = {
        'page_obj': page_obj,
        'total_registros': total_registros,
        'total_creaciones': total_creaciones,
        'total_lecturas': total_lecturas,
        'total_actualizaciones': total_actualizaciones,
        'total_eliminaciones': total_eliminaciones,
        'total_errores': total_errores,
        'usuario_filter': usuario_filter,
        'accion_filter': accion_filter,
        'metodo_filter': metodo_filter,
        'modelo_filter': modelo_filter,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'solo_exitosos': solo_exitosos,
    }
    return render(request, 'auditoria/lista_auditoria.html', context)

@login_required
@user_passes_test(es_admin_ti_o_superuser, login_url='login')
def detalle_auditoria(request, id):
    """Detalle de un registro de auditoría"""
    registro = Auditoria.objects.select_related('usuario', 'content_type').get(id=id)
    
    context = {
        'registro': registro,
    }
    return render(request, 'auditoria/detalle_auditoria.html', context)

