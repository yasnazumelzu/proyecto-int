from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente  # si ya existe la app pacientes

@login_required
def dashboard_admin(request):
    pacientes = Paciente.objects.all()  # Mostrar lista de pacientes
    return render(request, 'administrativo/dashboard.html', {'pacientes': pacientes})
