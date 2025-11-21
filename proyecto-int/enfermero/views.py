from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from pacientes.models import Paciente
from .models import ControlEnfermeria
from .forms import ControlEnfermeriaForm

@login_required
def dashboard_enfermero(request):
    """Dashboard principal del enfermero"""
    pacientes = Paciente.objects.all()
    
    # Estadísticas dinámicas
    pacientes_observacion = pacientes.count()  # Todos los pacientes están en observación
    controles_realizados = ControlEnfermeria.objects.count()
    alertas_medicacion = ControlEnfermeria.objects.filter(alertas=True).count()
    
    # Controles recientes
    controles_recientes = ControlEnfermeria.objects.all()[:5]
    
    context = {
        'pacientes': pacientes,
        'pacientes_observacion': pacientes_observacion,
        'controles_realizados': controles_realizados,
        'alertas_medicacion': alertas_medicacion,
        'controles_recientes': controles_recientes,
    }
    return render(request, 'enfermero/dashboard.html', context)

@login_required
def registrar_control(request):
    """Registrar un nuevo control de enfermería"""
    if request.method == 'POST':
        form = ControlEnfermeriaForm(request.POST)
        if form.is_valid():
            control = form.save(commit=False)
            control.usuario_registro = request.user
            control.save()
            messages.success(request, f'Control registrado exitosamente para {control.paciente.nombre}.')
            return redirect('lista_controles')
    else:
        form = ControlEnfermeriaForm()
    
    return render(request, 'enfermero/registrar_control.html', {'form': form})

@login_required
def lista_controles(request):
    """Lista todos los controles de enfermería"""
    controles = ControlEnfermeria.objects.all().select_related('paciente', 'usuario_registro').order_by('-fecha_control')
    
    # Filtros
    paciente_filter = request.GET.get('paciente', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    solo_alertas = request.GET.get('solo_alertas', '')
    
    if paciente_filter:
        controles = controles.filter(paciente__id=paciente_filter)
    if fecha_desde:
        controles = controles.filter(fecha_control__date__gte=fecha_desde)
    if fecha_hasta:
        controles = controles.filter(fecha_control__date__lte=fecha_hasta)
    if solo_alertas:
        controles = controles.filter(alertas=True)
    
    context = {
        'controles': controles,
        'pacientes': Paciente.objects.all(),
        'paciente_filter': paciente_filter,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'solo_alertas': solo_alertas,
    }
    return render(request, 'enfermero/lista_controles.html', context)

@login_required
def consultar_pacientes(request):
    """Consultar lista de pacientes con su información"""
    pacientes = Paciente.objects.all().prefetch_related('controles_enfermeria')
    
    # Filtros
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        pacientes = pacientes.filter(
            Q(nombre__icontains=busqueda) |
            Q(rut__icontains=busqueda) |
            Q(diagnostico__icontains=busqueda)
        )
    
    # Agregar información de controles recientes
    pacientes_con_info = []
    for paciente in pacientes:
        ultimo_control = paciente.controles_enfermeria.first()
        total_controles = paciente.controles_enfermeria.count()
        pacientes_con_info.append({
            'paciente': paciente,
            'ultimo_control': ultimo_control,
            'total_controles': total_controles,
        })
    
    context = {
        'pacientes_con_info': pacientes_con_info,
        'busqueda': busqueda,
    }
    return render(request, 'enfermero/consultar_pacientes.html', context)

@login_required
def detalle_paciente_enfermero(request, id):
    """Detalle de un paciente con todos sus controles"""
    paciente = get_object_or_404(Paciente, id=id)
    controles = ControlEnfermeria.objects.filter(paciente=paciente).order_by('-fecha_control')
    
    context = {
        'paciente': paciente,
        'controles': controles,
    }
    return render(request, 'enfermero/detalle_paciente.html', context)
