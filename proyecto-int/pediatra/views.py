from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from pacientes.models import RecienNacido
from .models import AltaRecienNacido
from .forms import AltaRecienNacidoForm

@login_required
def dashboard_pediatra(request):
    """Dashboard principal del pediatra"""
    # Verificar que el usuario sea pediatra
    if not (hasattr(request.user, 'rol') and request.user.rol == 'pediatra'):
        messages.error(request, 'No tiene permisos para acceder a esta sección.')
        return redirect('login')
    
    # Estadísticas
    total_recien_nacidos = RecienNacido.objects.count()
    recien_nacidos_sin_alta = RecienNacido.objects.filter(alta__isnull=True).count()
    altas_registradas = AltaRecienNacido.objects.filter(pediatra_responsable=request.user).count()
    # Si fecha_nacimiento es DateField, usar directamente; si es DateTimeField, usar __date
    recien_nacidos_hoy = RecienNacido.objects.filter(fecha_nacimiento=timezone.now().date()).count()
    
    # Recién nacidos recientes
    recien_nacidos_recientes = RecienNacido.objects.filter(alta__isnull=True).order_by('-fecha_nacimiento')[:5]
    
    context = {
        'total_recien_nacidos': total_recien_nacidos,
        'recien_nacidos_sin_alta': recien_nacidos_sin_alta,
        'altas_registradas': altas_registradas,
        'recien_nacidos_hoy': recien_nacidos_hoy,
        'recien_nacidos_recientes': recien_nacidos_recientes,
    }
    return render(request, 'pediatra/dashboard.html', context)

@login_required
def lista_recien_nacidos(request):
    """Lista de recién nacidos"""
    if not (hasattr(request.user, 'rol') and request.user.rol == 'pediatra'):
        messages.error(request, 'No tiene permisos para acceder a esta sección.')
        return redirect('login')
    
    recien_nacidos = RecienNacido.objects.all().select_related('paciente_madre').order_by('-fecha_nacimiento')
    
    # Filtros
    busqueda = request.GET.get('busqueda', '')
    solo_sin_alta = request.GET.get('solo_sin_alta', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    
    if solo_sin_alta:
        recien_nacidos = recien_nacidos.filter(alta__isnull=True)
    if busqueda:
        recien_nacidos = recien_nacidos.filter(
            Q(nombre__icontains=busqueda) |
            Q(apellido_paterno__icontains=busqueda) |
            Q(paciente_madre__nombre__icontains=busqueda) |
            Q(paciente_madre__rut__icontains=busqueda)
        )
    if fecha_desde:
        recien_nacidos = recien_nacidos.filter(fecha_nacimiento__gte=fecha_desde)
    if fecha_hasta:
        recien_nacidos = recien_nacidos.filter(fecha_nacimiento__lte=fecha_hasta)
    
    context = {
        'recien_nacidos': recien_nacidos,
        'busqueda': busqueda,
        'solo_sin_alta': solo_sin_alta,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
    }
    return render(request, 'pediatra/lista_recien_nacidos.html', context)

@login_required
def detalle_recien_nacido(request, id):
    """Detalle de un recién nacido"""
    if not (hasattr(request.user, 'rol') and request.user.rol == 'pediatra'):
        messages.error(request, 'No tiene permisos para acceder a esta sección.')
        return redirect('login')
    
    recien_nacido = get_object_or_404(RecienNacido, id=id)
    alta = getattr(recien_nacido, 'alta', None)
    
    context = {
        'recien_nacido': recien_nacido,
        'alta': alta,
    }
    return render(request, 'pediatra/detalle_recien_nacido.html', context)

@login_required
def registrar_alta_recien_nacido(request, recien_nacido_id=None):
    """Registrar alta de un recién nacido"""
    if not (hasattr(request.user, 'rol') and request.user.rol == 'pediatra'):
        messages.error(request, 'No tiene permisos para acceder a esta sección.')
        return redirect('login')
    
    recien_nacido = None
    if recien_nacido_id:
        recien_nacido = get_object_or_404(RecienNacido, id=recien_nacido_id)
        # Verificar si ya tiene alta
        if hasattr(recien_nacido, 'alta'):
            messages.info(request, 'Este recién nacido ya tiene un alta registrada.')
            return redirect('detalle_recien_nacido', id=recien_nacido.id)
    
    if request.method == 'POST':
        form = AltaRecienNacidoForm(request.POST)
        if form.is_valid():
            alta = form.save(commit=False)
            alta.pediatra_responsable = request.user
            if recien_nacido:
                alta.recien_nacido = recien_nacido
            alta.save()
            messages.success(request, f'Alta registrada exitosamente para {alta.recien_nacido.nombre}.')
            return redirect('detalle_recien_nacido', id=alta.recien_nacido.id)
    else:
        initial = {}
        if recien_nacido:
            initial['recien_nacido'] = recien_nacido
            # Prellenar peso al alta con el peso actual
            initial['peso_alta'] = recien_nacido.peso
        form = AltaRecienNacidoForm(initial=initial)
    
    context = {
        'form': form,
        'recien_nacido': recien_nacido,
    }
    return render(request, 'pediatra/registrar_alta.html', context)

@login_required
def lista_altas_recien_nacidos(request):
    """Lista de altas de recién nacidos"""
    if not (hasattr(request.user, 'rol') and request.user.rol == 'pediatra'):
        messages.error(request, 'No tiene permisos para acceder a esta sección.')
        return redirect('login')
    
    altas = AltaRecienNacido.objects.all().select_related('recien_nacido', 'pediatra_responsable').order_by('-fecha_alta')
    
    # Filtros
    tipo_alta_filter = request.GET.get('tipo_alta', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    solo_mios = request.GET.get('solo_mios', '')
    
    if solo_mios:
        altas = altas.filter(pediatra_responsable=request.user)
    if tipo_alta_filter:
        altas = altas.filter(tipo_alta=tipo_alta_filter)
    if fecha_desde:
        altas = altas.filter(fecha_alta__date__gte=fecha_desde)
    if fecha_hasta:
        altas = altas.filter(fecha_alta__date__lte=fecha_hasta)
    
    context = {
        'altas': altas,
        'tipo_alta_filter': tipo_alta_filter,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'solo_mios': solo_mios,
    }
    return render(request, 'pediatra/lista_altas.html', context)

