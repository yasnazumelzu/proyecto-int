from django.shortcuts import redirect
from django.contrib.auth import logout
from django.shortcuts import render

def inicio(request):
    return render(request, 'usuarios/inicio.html')


def logout_view(request):
    """Cierra la sesión del usuario y redirige al login"""
    logout(request)
    return redirect('login')
