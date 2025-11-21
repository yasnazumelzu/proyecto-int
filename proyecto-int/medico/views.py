from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from pacientes.models import Paciente
from .models import ReporteMedico
from .forms import ReporteMedicoForm

@login_required
def dashboard_medico(request):
    """Dashboard principal del médico"""
    pacientes = Paciente.objects.all()
    
    # Estadísticas dinámicas
    pacientes_atendidos = ReporteMedico.objects.filter(
        medico_responsable=request.user
    ).values('paciente').distinct().count()
    
    consultas_pendientes = ReporteMedico.objects.filter(
        estado__in=['pendiente', 'en_proceso']
    ).count()
    
    reportes_clinicos = ReporteMedico.objects.filter(
        medico_responsable=request.user
    ).count()
    
    # Reportes recientes
    reportes_recientes = ReporteMedico.objects.filter(
        medico_responsable=request.user
    )[:5]
    
    context = {
        'pacientes': pacientes,
        'pacientes_atendidos': pacientes_atendidos,
        'consultas_pendientes': consultas_pendientes,
        'reportes_clinicos': reportes_clinicos,
        'reportes_recientes': reportes_recientes,
    }
    return render(request, 'medico/dashboard.html', context)

@login_required
def revisar_pacientes(request):
    """Revisar fichas clínicas de pacientes"""
    pacientes = Paciente.objects.all().prefetch_related('reportes_medicos', 'controles_enfermeria')
    
    # Filtros
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        pacientes = pacientes.filter(
            Q(nombre__icontains=busqueda) |
            Q(rut__icontains=busqueda) |
            Q(diagnostico__icontains=busqueda)
        )
    
    # Agregar información de reportes
    pacientes_con_info = []
    for paciente in pacientes:
        ultimo_reporte = paciente.reportes_medicos.first()
        total_reportes = paciente.reportes_medicos.count()
        pacientes_con_info.append({
            'paciente': paciente,
            'ultimo_reporte': ultimo_reporte,
            'total_reportes': total_reportes,
        })
    
    context = {
        'pacientes_con_info': pacientes_con_info,
        'busqueda': busqueda,
    }
    return render(request, 'medico/revisar_pacientes.html', context)

@login_required
def ficha_clinica(request, id):
    """Ficha clínica completa de un paciente"""
    paciente = get_object_or_404(Paciente, id=id)
    reportes = ReporteMedico.objects.filter(paciente=paciente).order_by('-fecha_reporte')
    controles = paciente.controles_enfermeria.all().order_by('-fecha_control')[:10] if hasattr(paciente, 'controles_enfermeria') else []
    
    context = {
        'paciente': paciente,
        'reportes': reportes,
        'controles': controles,
    }
    return render(request, 'medico/ficha_clinica.html', context)

@login_required
def registrar_reporte(request):
    """Registrar un nuevo reporte médico"""
    if request.method == 'POST':
        form = ReporteMedicoForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.medico_responsable = request.user
            reporte.save()
            messages.success(request, f'Reporte médico registrado exitosamente para {reporte.paciente.nombre}.')
            return redirect('dashboard_medico')
    else:
        form = ReporteMedicoForm()
    
    return render(request, 'medico/registrar_reporte.html', {'form': form})

@login_required
def lista_reportes(request):
    """Lista todos los reportes médicos"""
    reportes = ReporteMedico.objects.all().select_related('paciente', 'medico_responsable').order_by('-fecha_reporte')
    
    # Filtros
    paciente_filter = request.GET.get('paciente', '')
    estado_filter = request.GET.get('estado', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')
    solo_mios = request.GET.get('solo_mios', '')
    
    if solo_mios:
        reportes = reportes.filter(medico_responsable=request.user)
    if paciente_filter:
        reportes = reportes.filter(paciente__id=paciente_filter)
    if estado_filter:
        reportes = reportes.filter(estado=estado_filter)
    if fecha_desde:
        reportes = reportes.filter(fecha_reporte__date__gte=fecha_desde)
    if fecha_hasta:
        reportes = reportes.filter(fecha_reporte__date__lte=fecha_hasta)
    
    context = {
        'reportes': reportes,
        'pacientes': Paciente.objects.all(),
        'paciente_filter': paciente_filter,
        'estado_filter': estado_filter,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'solo_mios': solo_mios,
    }
    return render(request, 'medico/lista_reportes.html', context)

@login_required
def detalle_reporte(request, id):
    """Detalle de un reporte médico"""
    reporte = get_object_or_404(ReporteMedico, id=id)
    
    context = {
        'reporte': reporte,
    }
    return render(request, 'medico/detalle_reporte.html', context)
