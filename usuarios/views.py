from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(request, user)
            grupos = [g.name for g in user.groups.all()]
            if 'Médico' in grupos:
                return redirect('dashboard_medico')
            elif 'Matrona' in grupos:
                return redirect('dashboard_matrona')
            elif 'Enfermero' in grupos:
                return redirect('dashboard_enfermero')
            elif 'Administrativo' in grupos:
                return redirect('dashboard_admin')
    return render(request, 'login.html', {'form': form})
