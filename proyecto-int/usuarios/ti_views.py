from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import Group, Permission
from django.db.models import Count, Q
from django.utils import timezone
from django.contrib.sessions.models import Session
from .models import Usuario
from .forms import UsuarioForm, UsuarioEditForm, GrupoForm
from pacientes.models import Paciente, RecienNacido
from administrativos.models import Admision, Pago

def es_admin_ti(user):
    """Verifica si el usuario es administrador TI"""
    return user.is_authenticated and (user.is_superuser or (hasattr(user, 'rol') and user.rol == 'ti'))

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def dashboard_ti(request):
    """Dashboard principal del administrador TI"""
    # Estadísticas de usuarios
    total_usuarios = Usuario.objects.count()
    usuarios_activos = Usuario.objects.filter(is_active=True).count()
    usuarios_inactivos = Usuario.objects.filter(is_active=False).count()
    usuarios_por_rol = Usuario.objects.values('rol').annotate(total=Count('id'))
    
    # Estadísticas de grupos
    total_grupos = Group.objects.count()
    
    # Estadísticas del sistema
    total_pacientes = Paciente.objects.count()
    total_recien_nacidos = RecienNacido.objects.count()
    total_admisiones = Admision.objects.count()
    total_pagos = Pago.objects.count()
    
    # Sesiones activas
    sesiones_activas = Session.objects.filter(expire_date__gte=timezone.now()).count()
    
    # Usuarios recientes
    usuarios_recientes = Usuario.objects.filter(
        date_joined__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    
    # Últimos usuarios creados
    ultimos_usuarios = Usuario.objects.all().order_by('-date_joined')[:5]
    
    context = {
        'total_usuarios': total_usuarios,
        'usuarios_activos': usuarios_activos,
        'usuarios_inactivos': usuarios_inactivos,
        'usuarios_por_rol': usuarios_por_rol,
        'total_grupos': total_grupos,
        'total_pacientes': total_pacientes,
        'total_recien_nacidos': total_recien_nacidos,
        'total_admisiones': total_admisiones,
        'total_pagos': total_pagos,
        'sesiones_activas': sesiones_activas,
        'usuarios_recientes': usuarios_recientes,
        'ultimos_usuarios': ultimos_usuarios,
    }
    return render(request, 'ti/dashboard.html', context)

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def lista_usuarios(request):
    """Lista todos los usuarios del sistema"""
    usuarios = Usuario.objects.all().order_by('-date_joined')
    
    # Filtros
    rol_filter = request.GET.get('rol', '')
    estado_filter = request.GET.get('estado', '')
    busqueda = request.GET.get('busqueda', '')
    
    if rol_filter:
        usuarios = usuarios.filter(rol=rol_filter)
    if estado_filter == 'activo':
        usuarios = usuarios.filter(is_active=True)
    elif estado_filter == 'inactivo':
        usuarios = usuarios.filter(is_active=False)
    if busqueda:
        usuarios = usuarios.filter(
            Q(username__icontains=busqueda) |
            Q(first_name__icontains=busqueda) |
            Q(last_name__icontains=busqueda) |
            Q(email__icontains=busqueda)
        )
    
    context = {
        'usuarios': usuarios,
        'rol_filter': rol_filter,
        'estado_filter': estado_filter,
        'busqueda': busqueda,
    }
    return render(request, 'ti/lista_usuarios.html', context)

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def crear_usuario(request):
    """Crear un nuevo usuario"""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuario {usuario.username} creado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm()
    
    return render(request, 'ti/crear_usuario.html', {'form': form})

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def editar_usuario(request, id):
    """Editar un usuario existente"""
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        form = UsuarioEditForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente.')
            return redirect('lista_usuarios')
    else:
        form = UsuarioEditForm(instance=usuario)
    
    return render(request, 'ti/editar_usuario.html', {'form': form, 'usuario': usuario})

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def eliminar_usuario(request, id):
    """Eliminar un usuario"""
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente.')
        return redirect('lista_usuarios')
    
    return render(request, 'ti/eliminar_usuario.html', {'usuario': usuario})

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def cambiar_estado_usuario(request, id):
    """Activar o desactivar un usuario"""
    usuario = get_object_or_404(Usuario, id=id)
    usuario.is_active = not usuario.is_active
    usuario.save()
    
    estado = "activado" if usuario.is_active else "desactivado"
    messages.success(request, f'Usuario {usuario.username} {estado} exitosamente.')
    return redirect('lista_usuarios')

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def resetear_password(request, id):
    """Resetear la contraseña de un usuario"""
    usuario = get_object_or_404(Usuario, id=id)
    
    if request.method == 'POST':
        nueva_password = request.POST.get('nueva_password')
        confirmar_password = request.POST.get('confirmar_password')
        
        if nueva_password and nueva_password == confirmar_password:
            usuario.set_password(nueva_password)
            usuario.save()
            messages.success(request, f'Contraseña de {usuario.username} reseteada exitosamente.')
            return redirect('lista_usuarios')
        else:
            messages.error(request, 'Las contraseñas no coinciden.')
    
    return render(request, 'ti/resetear_password.html', {'usuario': usuario})

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def lista_grupos(request):
    """Lista todos los grupos del sistema"""
    grupos = Group.objects.all().annotate(
        total_usuarios=Count('user')
    ).order_by('name')
    
    context = {
        'grupos': grupos,
    }
    return render(request, 'ti/lista_grupos.html', context)

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def detalle_grupo(request, id):
    """Detalle de un grupo con sus usuarios y permisos"""
    grupo = get_object_or_404(Group, id=id)
    usuarios_grupo = grupo.user_set.all()
    permisos_grupo = grupo.permissions.all()
    
    context = {
        'grupo': grupo,
        'usuarios_grupo': usuarios_grupo,
        'permisos_grupo': permisos_grupo,
    }
    return render(request, 'ti/detalle_grupo.html', context)

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def sesiones_activas(request):
    """Lista de sesiones activas en el sistema"""
    sesiones = Session.objects.filter(expire_date__gte=timezone.now())
    usuarios_sesion = []
    
    for sesion in sesiones:
        try:
            uid = sesion.get_decoded().get('_auth_user_id')
            if uid:
                usuario = Usuario.objects.get(id=uid)
                usuarios_sesion.append({
                    'usuario': usuario,
                    'sesion': sesion,
                    'fecha_expiracion': sesion.expire_date,
                })
        except:
            continue
    
    context = {
        'usuarios_sesion': usuarios_sesion,
        'total_sesiones': len(usuarios_sesion),
    }
    return render(request, 'ti/sesiones_activas.html', context)

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def cerrar_sesion_usuario(request, session_key):
    """Cerrar una sesión específica"""
    try:
        sesion = Session.objects.get(session_key=session_key)
        sesion.delete()
        messages.success(request, 'Sesión cerrada exitosamente.')
    except Session.DoesNotExist:
        messages.error(request, 'Sesión no encontrada.')
    
    return redirect('sesiones_activas')

@login_required
@user_passes_test(es_admin_ti, login_url='login')
def estadisticas_sistema(request):
    """Estadísticas detalladas del sistema"""
    # Estadísticas por rol
    usuarios_por_rol = []
    for rol_code, rol_name in Usuario.ROLES:
        total = Usuario.objects.filter(rol=rol_code).count()
        activos = Usuario.objects.filter(rol=rol_code, is_active=True).count()
        inactivos = Usuario.objects.filter(rol=rol_code, is_active=False).count()
        usuarios_por_rol.append({
            'rol': rol_code,
            'rol_display': rol_name,
            'total': total,
            'activos': activos,
            'inactivos': inactivos
        })
    
    # Estadísticas de actividad
    usuarios_ultimo_mes = Usuario.objects.filter(
        date_joined__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    
    usuarios_ultima_semana = Usuario.objects.filter(
        date_joined__gte=timezone.now() - timezone.timedelta(days=7)
    ).count()
    
    # Estadísticas de datos
    pacientes_ultimo_mes = Paciente.objects.filter(
        fecha_ingreso__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    
    recien_nacidos_ultimo_mes = RecienNacido.objects.filter(
        fecha_nacimiento__gte=timezone.now() - timezone.timedelta(days=30)
    ).count()
    
    context = {
        'usuarios_por_rol': usuarios_por_rol,
        'usuarios_ultimo_mes': usuarios_ultimo_mes,
        'usuarios_ultima_semana': usuarios_ultima_semana,
        'pacientes_ultimo_mes': pacientes_ultimo_mes,
        'recien_nacidos_ultimo_mes': recien_nacidos_ultimo_mes,
    }
    return render(request, 'ti/estadisticas_sistema.html', context)

