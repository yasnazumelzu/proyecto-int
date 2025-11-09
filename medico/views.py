from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pacientes.models import Paciente

@login_required
def dashboard_medico(request):
    pacientes = Paciente.objects.all()
    return render(request, 'medico/dashboard.html', {'pacientes': pacientes})
