from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente, RecienNacido  # Importar el modelo de pacientes

@login_required
def dashboard_matrona(request):
    pacientes = Paciente.objects.all()  # Obtener todos los pacientes
    # Calcular estadísticas
    total_partos = RecienNacido.objects.count()
    total_controles = pacientes.count()  # Simplificado, puedes ajustar según tu modelo
    total_recien_nacidos = RecienNacido.objects.count()
    
    context = {
        'pacientes': pacientes,
        'total_partos': total_partos,
        'total_controles': total_controles,
        'total_recien_nacidos': total_recien_nacidos,
    }
    return render(request, 'matrona/dashboard.html', context)

@login_required
def registrar_nacimiento(request):
    """Vista para seleccionar paciente y registrar nacimiento"""
    pacientes = Paciente.objects.all().order_by('nombre')
    return render(request, 'matrona/registrar_nacimiento.html', {'pacientes': pacientes})

@login_required
def seguimiento_materno(request):
    """Vista para seguimiento materno - lista de pacientes"""
    pacientes = Paciente.objects.all().order_by('nombre')
    return render(request, 'matrona/seguimiento_materno.html', {'pacientes': pacientes})
