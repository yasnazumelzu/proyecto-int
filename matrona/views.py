from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente  # Importar el modelo de pacientes

@login_required
def dashboard_matrona(request):
    pacientes = Paciente.objects.all()  # Obtener todos los pacientes
    return render(request, 'matrona/dashboard.html', {'pacientes': pacientes})
