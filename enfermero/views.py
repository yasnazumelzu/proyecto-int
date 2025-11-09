from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente  # Importa el modelo Paciente

@login_required
def dashboard_enfermero(request):
    pacientes = Paciente.objects.all()  # Carga todos los pacientes
    return render(request, 'enfermero/dashboard.html', {'pacientes': pacientes})
