from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Paciente, RecienNacido
from .forms import PacienteForm, RecienNacidoForm

@login_required
def lista_pacientes(request):
    pacientes = Paciente.objects.all().order_by('nombre')
    return render(request, 'pacientes/lista_pacientes.html', {'pacientes': pacientes})

@login_required
def detalle_paciente(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    return render(request, 'pacientes/detalle_paciente.html', {'paciente': paciente})

@login_required
def nuevo_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    return render(request, 'pacientes/nuevo_paciente.html', {'form': form})

@login_required
def nuevo_recien_nacido(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    if request.method == 'POST':
        form = RecienNacidoForm(request.POST)
        if form.is_valid():
            recien = form.save(commit=False)
            recien.paciente_madre = paciente
            recien.save()
            return redirect('detalle_paciente', id=paciente.id)
    else:
        form = RecienNacidoForm()
    return render(request, 'pacientes/nuevo_recien_nacido.html', {'form': form, 'paciente': paciente})
